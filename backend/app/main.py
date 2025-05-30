import os
import uuid

import aiofiles
from app.models import ConversionJobMessage, ConversionJobStatus
from app.tasks import convert_pptx_to_pdf_task
from app.utils.redis import get_redis_client
from celery.result import AsyncResult
from celery_worker.celery_app import celery_app
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="PPTX to PDF Conversion API", version="1.0.0")

# Add CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to the PPTX Upload API"}


@app.post("/convert/pptx-to-pdf")
async def convert_pptx_to_pdf(file: UploadFile = File(...)):
    """
    Endpoint to convert PPTX to PDF.
    Returns job ID for status tracking.
    """
    # Validate file type
    if not file.filename or not file.filename.endswith(".pptx"):
        raise HTTPException(status_code=400, detail="Only .pptx files are allowed")

    # Ensure temporary directory exists for file storage
    TMP_DIR = "/tmp"
    os.makedirs(TMP_DIR, exist_ok=True)

    # Create a unique ID for this conversion
    job_id = str(uuid.uuid4())

    # Generate all the necessary file paths for this conversion job
    input_filename = f"{job_id}_{file.filename}"
    output_filename = f"{job_id}_{file.filename.replace('.pptx', '.pdf')}"

    input_path = os.path.join(TMP_DIR, input_filename)
    output_path = os.path.join(TMP_DIR, output_filename)
    s3_key = f"converted-pdfs/{output_filename}"

    try:
        async with aiofiles.open(input_path, "wb") as file_buffer:
            while content := await file.read(8192):
                await file_buffer.write(content)

        task = convert_pptx_to_pdf_task.delay(input_path, output_path, s3_key)

        return JSONResponse(
            {
                "status": ConversionJobStatus.PENDING,
                "message": "Conversion job queued successfully",
                "job_id": task.id,
            }
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        return JSONResponse(
            {
                "status": ConversionJobStatus.ERROR,
                "message": "Failed to process the file",
                "job_id": job_id,
            }
        )

    except Exception as e:
        # Handle unexpected errors
        return JSONResponse(
            {
                "status": ConversionJobStatus.ERROR,
                "message": f"An error occurred: {str(e)}",
                "job_id": job_id,
            },
            status_code=500,
        )


@app.get("/status/{job_id}")
async def get_conversion_status(job_id: str):
    """
    Endpoint to get the status of a conversion job.
    Returns job status and any messages.
    """
    task = AsyncResult(job_id, app=celery_app)

    if not task:
        raise HTTPException(status_code=404, detail="Job not found")

    # State mapping
    state_mappings = {
        "PENDING": {
            "status": ConversionJobStatus.PENDING,
            "message": ConversionJobMessage.PENDING,
            "job_id": job_id,
        },
        "PROGRESS": {
            "status": ConversionJobStatus.IN_PROGRESS,
            "message": ConversionJobMessage.IN_PROGRESS,
            "job_id": job_id,
        },
        "SUCCESS": {
            "status": ConversionJobStatus.COMPLETED,
            "message": ConversionJobMessage.COMPLETED,
            "job_id": job_id,
        },
        "FAILURE": {
            "status": ConversionJobStatus.ERROR,
            "message": ConversionJobMessage.ERROR,
            "job_id": job_id,
        },
    }

    # Base response
    response_data = {
        "status": ConversionJobStatus.UNKNOWN,
        "message": ConversionJobMessage.UNKNOWN,
        "job_id": job_id,
    }

    # Check for known states
    for state, mapping in state_mappings.items():
        if task.state == state:
            response_data.update(mapping)

            # Special handling for SUCCESS state
            if state == "SUCCESS":
                redis_client = get_redis_client()
                s3_url = redis_client.get(job_id)

                response_data["s3_url"] = s3_url
            break

    return JSONResponse(response_data)
