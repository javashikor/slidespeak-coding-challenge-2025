import os

import boto3
from app.utils.config import (
    AWS_ACCESS_KEY_ID,
    AWS_REGION,
    AWS_S3_BUCKET,
    AWS_SECRET_ACCESS_KEY,
)


def upload_to_s3(file_path: str, object_name: str) -> str:
    """
    Upload a file to S3 synchronously and return a presigned download URL.
    """
    try:
        # Create S3 client
        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION,
        )

        # Read file content
        with open(file_path, "rb") as file:
            file_content = file.read()

        # Upload to S3
        s3.put_object(
            Bucket=AWS_S3_BUCKET,
            Key=object_name,
            Body=file_content,
            ContentType="application/pdf",
        )

        # Generate presigned URL
        url = s3.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": AWS_S3_BUCKET,
                "Key": object_name,
                "ResponseContentDisposition": f'attachment; filename="{os.path.basename(file_path)}"',
            },
            ExpiresIn=3600,  # 1 hour
        )

        return url

    except Exception as e:
        raise Exception(f"Error uploading to S3: {str(e)}")
