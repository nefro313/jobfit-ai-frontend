import requests
from app.core.logger import get_logger
from app.core.exceptions import CustomException

from app.core.config import settings


API_BASE_URL = settings.API_BASE_URL
    
logger =get_logger(__name__)


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
        response.raise_for_status() 

        # Safely extract data

        return response

    except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error communicating with AI service: {str(e)}")

    except ValueError:
          logger.error( "⚠️ Response was not valid JSON.")

