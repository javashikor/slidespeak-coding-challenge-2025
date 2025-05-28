import aiofiles
import httpx

from app.utils.config import get_settings

UNOSERVER_URL = get_settings().UNOSERVER_URL


async def convert_with_unoserver(input_path: str, output_path: str) -> bool:
    """
    Convert PPTX to PDF using unoserver
    """
    try:
        async with httpx.AsyncClient(timeout=300.0) as client:  # 5 minute timeout
            # Read the input file
            async with aiofiles.open(input_path, "rb") as f:
                file_content = await f.read()

            # Prepare the request
            files = {
                "file": (
                    "presentation.pptx",
                    file_content,
                    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                )
            }

            data = {"convert-to": "pdf"}

            # Make request to unoserver
            response = await client.post(
                f"{UNOSERVER_URL}/request", files=files, data=data
            )

            if response.status_code == 200:
                # Save the converted PDF
                async with aiofiles.open(output_path, "wb") as f:
                    await f.write(response.content)
                return True
            else:
                print(
                    f"unoserver conversion failed: {response.status_code} - {response.text}"
                )
                return False

    except Exception as e:
        print(f"unoserver conversion error: {str(e)}")
        return False
