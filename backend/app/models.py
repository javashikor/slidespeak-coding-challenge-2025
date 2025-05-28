from enum import StrEnum
from typing import Optional

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_S3_BUCKET: str
    AWS_REGION: str = "eu-west-2"
    UNOSERVER_URL: str = "http://localhost:2004"

    model_config = SettingsConfigDict(env_file="../../.env")


class ConversionJobMessage(StrEnum):
    JOB_CREATED = "Job created successfully."
    JOB_STARTED = "Job started."
    JOB_COMPLETED = "Job completed successfully."
    JOB_FAILED = "Job failed."
    JOB_CANCELLED = "Job cancelled."
    JOB_PROGRESS_UPDATE = "Job progress updated."
    JOB_NOT_FOUND = "Job not found."
    INVALID_JOB_ID = "Invalid job ID provided."
    UNAUTHORIZED_ACCESS = "Unauthorized access to the job."
    SERVER_ERROR = "An error occurred on the server."
    FILE_NOT_FOUND = "The specified file was not found."
    # Additional messages for the conversion process
    SAVING_FILE = "Saving uploaded file..."
    CONVERTING = "Converting PPTX to PDF..."
    UPLOADING_S3 = "Uploading to S3..."
    CONVERSION_FAILED = "Conversion failed"
    FILE_NOT_FOUND_AFTER_CONVERSION = "Converted file not found"
    CONVERSION_COMPLETE = "Conversion completed successfully"


class ConversionJobStatus(StrEnum):
    PENDING = "pending"
    UPLOADING = "uploading"
    CONVERTING = "converting"
    UPLOADING_S3 = "uploading_s3"
    COMPLETE = "complete"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ERROR = "error"


class ConversionJobStage(StrEnum):
    INITIAL = "initial"
    UPLOAD = "upload"
    CONVERSION = "conversion"
    S3_UPLOAD = "s3_upload"
    COMPLETE = "complete"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"
    CANCELLED = "cancelled"


class ConversionJob(BaseModel):
    job_id: str
    status: str = ConversionJobStatus.PENDING
    progress: int = 0
    message: str = ConversionJobMessage.JOB_CREATED
    stage: str = ConversionJobStage.INITIAL
    download_url: Optional[str] = None

    class Config:
        orm_mode = True

    def update(self, updates: dict):
        for key, value in updates.items():
            setattr(self, key, value)


class ConversionJobList(BaseModel):
    jobs: list[ConversionJob] = []

    def add_job(self, job: ConversionJob):
        self.jobs.append(job)

    def get_job(self, job_id: str) -> Optional[ConversionJob]:
        for job in self.jobs:
            if job.job_id == job_id:
                return job
        return None

    def update_job(self, job_id: str, updates: dict):
        job = self.get_job(job_id)
        if job:
            job.update(updates)

    def remove_job(self, job_id: str):
        self.jobs = [job for job in self.jobs if job.job_id != job_id]

    def __contains__(self, job_id: str) -> bool:
        """Allow 'job_id in conversion_jobs' syntax"""
        return self.get_job(job_id) is not None

    def __getitem__(self, job_id: str) -> ConversionJob:
        """Allow 'conversion_jobs[job_id]' syntax"""
        job = self.get_job(job_id)
        if job is None:
            raise KeyError(f"Job with ID {job_id} not found")
        return job
