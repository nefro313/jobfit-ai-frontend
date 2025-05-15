from typing import Optional
import requests
from app.core.config import API_BASE_URL
from app.core.logger import get_logger
from app.core.config import settings

API_BASE_URL = settings.API_BASE_URL
logger = get_logger(__name__)

def hr_qa_client(query: str) -> Optional[str]:
    """
    Get HR policy answer from the QA service
    
    Args:
        query: HR-related question to answer (3-500 characters)
        
    Returns:
        str: Answer text if successful
        None: If request fails or returns invalid response
    """
    try:
        response = requests.post(
            url=f"{API_BASE_URL}/api/hr-qa/answer",
            json={"query": query},  # Changed to json for better content-type handling
            timeout=10  # Add timeout to prevent hanging requests
        )
        
        # Log successful request metrics
        logger.debug(
            f"HR QA request completed - Status: {response.status_code}",
            extra={"query": query, "status_code": response.status_code}
        )
        # Process the response
        if response.status_code == 200:
            report = response.json().get("response", "No report found.")
            logger.info("Successfully retrieved job analysis report")
            logger.info("ATS check completed successfully")
            return report

            
        logger.warning("Received empty response from HR QA service")
        return None
        
    except requests.exceptions.RequestException as e:
        logger.error(
            "HR QA request failed",
            extra={"error": str(e), "query": query}
        )
    except ValueError as ve:  # Handle JSON decode errors
        logger.error(
            "Invalid JSON response from HR QA service",
            extra={"error": str(ve), "query": query}
        )
    
    return None