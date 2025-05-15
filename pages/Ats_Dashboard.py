"""
Streamlit ATS (Applicant Tracking System) Checker Page

This module provides a Streamlit interface for users to:
1. Upload their resume in PDF format
2. Input a job description
3. Get analysis of how well their resume matches the job description

The main functionality is delegated to the resume_analyser component.
"""

import streamlit as st
from app.components.resume_analyser import resume_analyzer
from app.core.logger import get_logger
from app.core.exceptions import CustomException

# Initialize logger
logger = get_logger(__name__)

def ats_checker():
    try:
        logger.info("Initializing ATS Checker page")
        
        st.title("Analyse Your Resume")
        st.write("Please upload your resume in PDF format.")
        
        resume_file = st.file_uploader(
            "Upload your resume (PDF)", 
            type=["pdf"],
            help="Only PDF files are accepted"
        )
        
        job_description = st.text_area(
            "Paste the job description here",
            help="Copy and paste the full job description for accurate analysis"
        )
        
        if resume_file is not None and job_description.strip() != "":
            return resume_analyzer(resume_file, job_description)
        
        # Optional: display a message before inputs are given
        else:
            st.info("Please upload a resume and paste the job description to continue.")

    except Exception as e:
        logger.critical(f"Unexpected error in ATS Checker page: {str(e)}")
        st.error("A system error occurred. Please refresh the page and try again.")
        raise CustomException(e)
if __name__ == "__main__":
    ats_checker()