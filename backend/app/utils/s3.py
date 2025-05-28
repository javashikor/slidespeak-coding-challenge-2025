import os

import aioboto3
import aiofiles
from app.utils.config import (
    AWS_ACCESS_KEY_ID,
    AWS_REGION,
    AWS_S3_BUCKET,
    AWS_SECRET_ACCESS_KEY,
)


async def upload_to_s3(file_path: str, object_name: str) -> str:

    print(f"Uploading {file_path} to S3 bucket {AWS_S3_BUCKET} as {object_name}")
    print(f"Using AWS region: {AWS_REGION}")
    print(f"Using AWS access key ID: {AWS_ACCESS_KEY_ID}")
    print(f"Using AWS secret access key: {AWS_SECRET_ACCESS_KEY}")

    session = aioboto3.Session()

    async with session.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    ) as s3:
        try:
            async with aiofiles.open(file_path, "rb") as file:
                file_content = await file.read()

            await s3.put_object(
                Bucket=AWS_S3_BUCKET,
                Key=object_name,
                Body=file_content,
                ContentType="application/pdf",
            )

            url = await s3.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": AWS_S3_BUCKET,
                    "Key": object_name,
                    "ResponseContentDisposition": f'attachment; filename="{os.path.basename(file_path)}"',
                },
                ExpiresIn=3600,
            )

            return url

        except Exception as e:
            raise Exception(f"Error uploading to S3: {str(e)}")
