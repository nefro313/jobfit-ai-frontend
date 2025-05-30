

import requests
from typing import Optional, Dict, Any, BinaryIO
from app.core.config import settings

from app.core.logger import get_logger
from app.core.exceptions import CustomException
#back-end api url
API_BASE_URL = settings.API_BASE_URL
logger = get_logger(__name__)

def check_resume_against_job_description(
    resume_file: BinaryIO, 
    job_description: str
) -> Optional[Dict[str, Any]]:
    """
    Submit a resume and job description to the ATS checker API and return the compatibility report.
    
    Args:
        resume_file: An open file object containing the resume (PDF format)
        job_description: String containing the job description text
        
    Returns:
        Dict containing the ATS compatibility report or None if the request failed
        
    Raises:
        CustomException: If there's an error during the API request
    """
    logger.info("Starting ATS compatibility check")
    logger.debug(f"Processing resume file: {resume_file.name}")
    
    try:
        # Prepare files and data for the request
        files = {
            "file": (resume_file.name, resume_file, "application/pdf")
        }
        data = {
            "job_description": job_description
        }
        
        logger.debug(f"Sending request to {API_BASE_URL}/api/ats-checker/check")
        
        # Make the API request
        response = requests.post(
            url=f"{API_BASE_URL}/api/ats-checker/check",
            files=files,
            data=data
        )
        
        # Process the response
        if response.status_code == 200:
            report = response.json().get("response", "No report found.")
            logger.info("Successfully retrieved job analysis report")
            logger.info("ATS check completed successfully")
            return report
        
    except requests.exceptions.RequestException as e:
        logger.error(f"ATS API request failed: {str(e)}")
        raise CustomException(e)
    except Exception as e:
        logger.error(f"Unexpected error during ATS check: {str(e)}")
        raise CustomException(e)