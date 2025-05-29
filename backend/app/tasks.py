# app/tasks.py
import os
import traceback

from app.utils.config import CELERY_BROKER_URL
from app.utils.convert import convert_with_unoserver
from app.utils.redis import get_redis_client
from app.utils.s3 import upload_to_s3
from celery_worker.celery_app import celery_app


@celery_app.task(
    bind=True,
    name="convert_pptx_to_pdf_task",
    max_retries=3,
    default_retry_delay=60,  # Retry after 1 minute
)
def convert_pptx_to_pdf_task(
    self, input_path: str, output_path: str, s3_key: str
) -> dict:

    task_id = self.request.id
    redis_client = get_redis_client()

    # Ensure input and output paths are absolute
    input_path = os.path.abspath(input_path)
    output_path = os.path.abspath(output_path)

    try:
        # Step 1: Validate input file
        self.update_state(
            state="STARTED",
            meta={
                "progress": 10,
                "status": "Validating input file...",
                "current_step": "validation",
            },
        )

        # validate_file_exists(input_path)

        # Step 2: Convert file
        self.update_state(
            state="PROGRESS",
            meta={
                "progress": 25,
                "status": "Converting PPTX to PDF...",
                "current_step": "conversion",
            },
        )

        success = convert_with_unoserver(input_path, output_path)

        if not success:
            raise Exception("Conversion failed with unoserver")

        # Step 3: Upload to S3
        self.update_state(
            state="PROGRESS",
            meta={
                "progress": 75,
                "status": "Uploading to cloud storage...",
                "current_step": "upload",
            },
        )

        s3_url = upload_to_s3(output_path, s3_key)

        if not s3_url:
            raise Exception("Failed to upload file to S3")

        # Step 4: Complete
        self.update_state(
            state="SUCCESS",
            meta={
                "progress": 100,
                "status": "Conversion completed successfully",
                "current_step": "completed",
            },
        )

        redis_client.setex(
            task_id,
            3600,  # Store for 1 hour
            s3_url,
        )

    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"

        self.update_state(
            state="FAILURE",
            meta={
                "progress": 0,
                "status": error_msg,
                "error": str(e),
                "error_type": "unexpected_error",
                "exc_type": type(e).__name__,
                "exc_message": traceback.format_exc().split("\n"),
            },
        )
        raise
    finally:
        # Cleanup files
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)