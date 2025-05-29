import os
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

# class Settings(BaseSettings):
#     AWS_ACCESS_KEY_ID: str
#     AWS_SECRET_ACCESS_KEY: str
#     AWS_S3_BUCKET: str
#     AWS_REGION: str
#     UNOSERVER_URL: str
#     FRONTEND_URL: str
#     BACKEND_URL: str

#     model_config = SettingsConfigDict(env_file="../.env")


class ConversionJobMessage(StrEnum):
    PENDING = "Job is pending"
    STARTED = "Job has started"
    IN_PROGRESS = "Job is in progress"
    COMPLETED = "Job has completed successfully"
    ERROR = "Job has failed with an error"
    UNKNOWN = "Unknown job status"


class ConversionJobStatus(StrEnum):
    PENDING = "pending"
    STARTED = "started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ERROR = "error"
    UNKNOWN = "unknown"
