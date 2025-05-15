import requests
from app.core.logger import get_logger
from app.core.exceptions import CustomException

API_BASE_URL = "http://localhost:8000"

    



def tailor_resume_and_guide(resume_file, job_posting_url, github_url, write_up):
    """
    Sends resume tailoring request to backend and returns AI-generated report.
    """

    # Build multipart/form-data for file upload
    files = {
        'file': (
            resume_file.name,  # Streamlit file uploader provides this
            resume_file.getvalue(),
            resume_file.type or "application/pdf"
        )
    }

    # Form data
    data = {
        "job_posting_url": job_posting_url,
        "github_url": github_url,
        "write_up": write_up
    }

    try:
        response = requests.post(
            url=f"{API_BASE_URL}/api/resume-builder/check", 
            files=files,
            data=data,

        )
        response.raise_for_status()  # raises HTTPError if not 200

        # Safely extract data
        resp_json = response.json()
        return resp_json

    except requests.exceptions.Timeout:
        return "⏳ Request timed out. Try again later."

    except requests.exceptions.RequestException as e:
        return f"❌ Error communicating with AI service: {str(e)}"

    except ValueError:
        return "⚠️ Response was not valid JSON."

