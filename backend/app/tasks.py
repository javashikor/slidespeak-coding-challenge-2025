# app/tasks.py
import os

from app.utils.convert import convert_with_unoserver
from app.utils.redis import get_redis_client
from app.utils.s3 import upload_to_s3
from celery_worker.celery_app import celery_app


def validate_file_exists(file_path: str):
    """
    Validate that the input file exists.
    Raises an exception if the file does not exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file does not exist: {file_path}")
    if not os.path.isfile(file_path):
        raise IsADirectoryError(f"Input path is not a file: {file_path}")


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

    try:
        # Step 1: Validate input file
        self.update_state(state="STARTED")

        # validate_file_exists(input_path)

        # Step 2: Convert file
        self.update_state(state="PROGRESS")

        success = convert_with_unoserver(input_path, output_path)

        if not success:
            raise Exception("Conversion failed with unoserver")

        # Step 3: Upload to S3
        self.update_state(state="PROGRESS")

        s3_url = upload_to_s3(output_path, s3_key)

        if not s3_url:
            raise Exception("Failed to upload file to S3")

        # Step 4: Complete
        self.update_state(state="SUCCESS")

        redis_client.setex(
            task_id,
            3600,  # Store for 1 hour
            s3_url,
        )

    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"

        self.update_state(state="FAILURE")
        raise
    finally:
        # Cleanup files
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
