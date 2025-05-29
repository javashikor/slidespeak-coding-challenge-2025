import requests
from app.utils.config import UNOSERVER_URL


def convert_with_unoserver(input_path: str, output_path: str) -> bool:
    """
    Synchronously convert PPTX to PDF using unoserver.
    """
    try:
        with open(input_path, "rb") as f:
            file_content = f.read()

        files = {
            "file": (
                "presentation.pptx",
                file_content,
                "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            )
        }

        data = {"convert-to": "pdf"}

        response = requests.post(
            f"{UNOSERVER_URL}/request",
            files=files,
            data=data,
            timeout=300,  # 5 minute timeout
        )

        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            return True
        else:
            print(
                f"unoserver conversion failed: {response.status_code} - {response.text}"
            )
            return False

    except Exception as e:
        print(f"unoserver conversion error: {str(e)}")
        return False
