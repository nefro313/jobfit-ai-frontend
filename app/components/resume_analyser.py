"""
Resume Analysis UI Module

This module provides UI functionality for uploading resumes, entering job descriptions,
and analyzing them through the ATS checker service.
"""

import streamlit as st
from typing import BinaryIO, Optional
import traceback

# Import custom components
from app.utils.api_clients.ats_client import check_resume_against_job_description
from app.core.logger import get_logger
from app.core.exceptions import CustomException

# Initialize logger
logger = get_logger(__name__)


def resume_analyzer(resume_file: Optional[BinaryIO], job_description: str) -> None:
    """
    Handle resume analysis UI workflow including file validation, API interaction,
    and result display.
    
    Args:
        resume_file: The uploaded resume file object or None if not uploaded
        job_description: String containing the job description text
        
    Returns:
        None - Updates the UI directly
    """
    try:
        logger.info("Resume analyzer function called")

                
            # Both inputs are provided, proceed with analysis
        logger.info("Starting resume analysis")
        
        # Call the ATS checker API
        return check_resume_against_job_description(
            resume_file, 
            job_description
        )


                    
    except CustomException as ce:
        logger.error(f"Custom exception in resume analysis: {str(ce)}")

    except Exception as e:
        logger.error(f"Unexpected error in resume analysis: {str(e)}")
        logger.debug(traceback.format_exc())
