import os
import uuid

import aiofiles
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.models import (
    ConversionJob,
    ConversionJobList,
    ConversionJobMessage,
    ConversionJobStage,
    ConversionJobStatus,
)
from app.utils.config import get_settings
from app.utils.convert import convert_with_unoserver
from app.utils.s3 import upload_to_s3

app = FastAPI(title="PPTX to PDF Conversion API", version="1.0.0")

# Get application environment settings
settings = get_settings()

# Add CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store conversion statuses (in production, use Redis or database)
conversion_jobs = ConversionJobList()


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
    os.makedirs("tmp", exist_ok=True)

    # Create a unique ID for this conversion
    job_id = str(uuid.uuid4())

    # Create and add job to the job list
    job = ConversionJob(
        job_id=job_id,
        status=ConversionJobStatus.PENDING,
        progress=0,
        message=ConversionJobMessage.JOB_CREATED,
        stage=ConversionJobStage.INITIAL,
    )
    conversion_jobs.add_job(job)

    # Generate all the necessary file paths for this conversion job
    input_filename = f"{job_id}_{file.filename}"
    output_filename = f"{job_id}_{file.filename.replace('.pptx', '.pdf')}"
    input_path = f"tmp/{input_filename}"
    output_path = f"tmp/{output_filename}"
    s3_key = f"converted-pdfs/{output_filename}"

    print(f"Input path: {input_path}, Output path: {output_path}, S3 key: {s3_key}")

    try:
        # Step 1: Save uploaded file to a temporary location
        conversion_jobs.update_job(
            job_id,
            {
                "status": ConversionJobStatus.UPLOADING,
                "progress": 10,
                "message": ConversionJobMessage.SAVING_FILE,
                "stage": ConversionJobStage.UPLOAD,
            },
        )

        async with aiofiles.open(input_path, "wb") as file_buffer:
            while content := await file.read(8192):
                await file_buffer.write(content)

        # Step 2: Convert PPTX to PDF
        conversion_jobs.update_job(
            job_id,
            {
                "status": ConversionJobStatus.IN_PROGRESS,
                "progress": 30,
                "message": ConversionJobMessage.CONVERTING,
                "stage": ConversionJobStage.PROCESSING,
            },
        )

        success = await convert_with_unoserver(input_path, output_path)

        if not success:
            conversion_jobs.update_job(
                job_id,
                {
                    "status": ConversionJobStatus.FAILED,
                    "progress": 0,
                    "message": ConversionJobMessage.CONVERSION_FAILED,
                    "stage": ConversionJobStage.ERROR,
                },
            )
            raise HTTPException(status_code=500, detail="Conversion failed")

        # Step 3: Upload to S3
        conversion_jobs.update_job(
            job_id,
            {
                "status": ConversionJobStatus.UPLOADING_S3,
                "progress": 70,
                "message": ConversionJobMessage.UPLOADING_S3,
                "stage": ConversionJobStage.S3_UPLOAD,
            },
        )

        s3_url = await upload_to_s3(output_path, s3_key)

        # Step 4: Complete job
        conversion_jobs.update_job(
            job_id,
            {
                "status": ConversionJobStatus.COMPLETE,
                "progress": 100,
                "message": ConversionJobMessage.CONVERSION_COMPLETE,
                "stage": ConversionJobStage.COMPLETE,
                "download_url": s3_url,
            },
        )

        return JSONResponse(
            {
                "success": True,
                "message": "Conversion completed successfully",
                "job_id": job_id,
                "download_url": s3_url,
            }
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle unexpected errors
        conversion_jobs.update_job(
            job_id,
            {
                "status": ConversionJobStatus.ERROR,
                "progress": 0,
                "message": f"Error: {str(e)}",
                "stage": ConversionJobStage.ERROR,
            },
        )
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Clean up temporary files
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)


@app.get("/status/{job_id}")
async def get_conversion_status(job_id: str):
    """Get the current status of a conversion job"""
    if job_id in conversion_jobs:
        return conversion_jobs[job_id]
    else:
        return {
            "status": ConversionJobStatus.ERROR,
            "message": ConversionJobMessage.JOB_NOT_FOUND,
        }
