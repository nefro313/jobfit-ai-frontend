
"""
Job Posting Analyzer Client Module

This module provides functionality to communicate with the job posting analyzer API
to analyze job postings from provided URLs.
"""

import requests
from typing import Optional, Dict, Any


# Import custom exceptions and logger
from app.core.exceptions import CustomException
from app.core.logger import get_logger
from app.core.config import settings
# Initialize logger for this module
logger = get_logger(__name__)

# API Base URL should be in config, but using a placeholder for now
API_BASE_URL = settings.API_BASE_URL

def analyze_job_posting(url: str) -> Optional[Dict[str, Any]]:
    """
    Analyze a job posting by sending the URL to the job analysis API.

    Args:
        url (str): The URL of the job posting to analyze

    Returns:
        Optional[Dict[str, Any]]: The analysis report as a dictionary if successful, None otherwise

    Raises:
        CustomException: If there's an error making the API request or processing the response
    """
    logger.info(f"Sending job posting URL for analysis: {url}")
    
    try:
        # Make the API request
        response = requests.post(
            url=f"{API_BASE_URL}/api/job-analysis/analyze", 
            data={"url": url},
        )
        
        # Log the response status
        logger.debug(f"Received response with status code: {response.status_code}")
        
        # Process the response
        if response.status_code == 200:
            report = response.json().get("response", "No report found.")
            logger.info("Successfully retrieved job analysis report")
            return report
        else:
            error_message = f"Failed to analyze job posting. Status code: {response.status_code}"
            logger.error(error_message)
            
            # Try to get error details if available
            try:
                error_details = response.json()
                logger.error(f"Error details: {error_details}")
            except Exception:
                logger.error("No error details available in response")
                
            return None
            
    except requests.RequestException as e:
        error_message = f"Request error while analyzing job posting: {str(e)}"
        logger.error(error_message)
        raise CustomException(e)
    except ValueError as e:
        error_message = f"Invalid response format from job analysis API: {str(e)}"
        logger.error(error_message)
        raise CustomException(e)
    except Exception as e:
        error_message = f"Unexpected error in job posting analysis: {str(e)}"
        logger.error(error_message)
        raise CustomException(e)