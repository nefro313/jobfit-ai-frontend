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
    logger.info("Resume analyzer function called")
    
    if st.button("Analyze"):
        logger.debug("Analyze button clicked")
        
        # Validate inputs
        if not resume_file:
            logger.warning("Resume file missing")
            st.warning("Please upload a resume file.")
            return
            
        if not job_description:
            logger.warning("Job description missing")
            st.warning("Please enter a job description.")
            return
            
        # Both inputs are provided, proceed with analysis
        try:
            with st.spinner("Analyzing your resume against job requirements..."):
                logger.info("Starting resume analysis")
                
                # Call the ATS checker API
                report = check_resume_against_job_description(
                    resume_file, 
                    job_description
                )
                
                # Display results
                if report:
                    logger.info("Resume analysis completed successfully")
                    st.success("Analysis complete!")
                    
                    # Display markdown report
                    st.markdown(report)
                    
                    # Log a snippet of the report (first 100 chars)
                    logger.debug(f"Report snippet: {report[:100]}...")
                else:
                    logger.error("Empty report returned from ATS checker")
                    st.error("Failed to analyze the resume. Please try again later.")
                    
        except CustomException as ce:
            logger.error(f"Custom exception in resume analysis: {str(ce)}")
            st.error(f"Analysis failed: {str(ce)}")
        except Exception as e:
            logger.error(f"Unexpected error in resume analysis: {str(e)}")
            logger.debug(traceback.format_exc())
            st.error("An unexpected error occurred. Please try again later.")