


"""
Streamlit ATS (Applicant Tracking System) Checker Page

This module provides a professional Streamlit interface for users to:
1. Upload their resume in PDF format
2. Input a job description
3. Get analysis of how well their resume matches the job description

The main functionality is delegated to the resume_analyser component.
"""

import streamlit as st
import time
from typing import Optional
import os
from datetime import datetime

from app.components.resume_analyser import resume_analyzer
from app.core.logger import get_logger
from app.core.exceptions import CustomException

# Initialize logger
logger = get_logger(__name__)

# Define color scheme and styling constants
PRIMARY_COLOR = "#4CAF50"
SECONDARY_COLOR = "#2196F3"
ACCENT_COLOR = "#FF9800"
BG_COLOR = "#F5F5F5"
TEXT_COLOR = "#212121"


def page_setup():
    """Configure the page with custom theme and layout."""
    try:
        st.set_page_config(
            page_title="ATS Resume Checker",
            page_icon="📄",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS styling
        st.markdown("""
        <style>
        .main {
            background-color: #F5F5F5;
            padding: 20px;
        }
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border: none;
            padding: 10px 24px;
            border-radius: 4px;
            transition-duration: 0.4s;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
        .stTextArea > div > div > textarea {
            border-radius: 4px;
            border: 1px solid #ddd;
        }
        .stUploadButton > div {
            border-radius: 4px;
            border: 1px solid #ddd;
        }
        .stProgress > div > div > div {
            background-color: #4CAF50;
        }
        h1 {
            color: #212121;
            font-weight: bold;
        }
        h2 {
            color: #424242;
        }
        .stAlert > div {
            border-radius: 4px;
            padding: 15px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        logger.debug("Page setup complete with custom styling")
    except Exception as e:
        logger.error(f"Error in page setup: {str(e)}")
        raise CustomException(e)


def display_header():
    """Display the header section with logo and title."""
    try:
        # Header with columns for logo and title
        col1, col2 = st.columns([1, 4])
        
        with col1:
            st.markdown("""
            <div style="text-align: center; padding: 10px;">
            <span style="font-size: 48px;">📄</span>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <h1 style="margin-bottom: 0px;">ATS Resume Checker</h1>
            <p style="color: #757575; margin-top: 0px;">
            Optimize your resume for Applicant Tracking Systems
            </p>
            """, unsafe_allow_html=True)
            
        # Divider
        st.markdown("<hr style='margin: 20px 0; border: 0; border-top: 1px solid #ddd;'>", unsafe_allow_html=True)
        
        logger.debug("Header section displayed")
    except Exception as e:
        logger.error(f"Error displaying header: {str(e)}")
        raise CustomException(e)


def display_sidebar():
    """Configure and display the sidebar with helpful information."""
    try:
        with st.sidebar:
            st.markdown("""
            <h2 style="text-align: center;">How it Works</h2>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            ### 1. Upload Your Resume
            Upload your resume in PDF format. This is the document that will be analyzed.
            
            ### 2. Paste Job Description
            Copy and paste the full job description from the position you're applying for.
            
            ### 3. Analyze
            Click the 'Analyze Resume' button to see how well your resume matches the job requirements.
            
            ### 4. Review Results
            - See your match score
            - Identify missing keywords
            - Get suggestions for improvement
            """)
            
        logger.debug("Sidebar information displayed")
    except Exception as e:
        logger.error(f"Error displaying sidebar: {str(e)}")
        raise CustomException(e)


def save_uploaded_file(uploaded_file) -> Optional[str]:
    """
    Save the uploaded file to a temporary location and return the path.
    
    Args:
        uploaded_file: The uploaded file from Streamlit
        
    Returns:
        Optional[str]: The path to the saved file, or None if saving failed
    """
    try:
        if uploaded_file is None:
            return None
            
        # Create temp directory if it doesn't exist
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Create a unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(temp_dir, f"{timestamp}_{uploaded_file.name}")
        
        # Save the file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        logger.info(f"Saved uploaded file to {file_path}")
        return file_path
        
    except Exception as e:
        logger.error(f"Error saving uploaded file: {str(e)}")
        return None


def display_input_section():
    """Display the input section for resume upload and job description."""
    try:
        # Use columns for layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <h3 style="color: #424242;">📤 Upload Your Resume</h3>
            """, unsafe_allow_html=True)
            
            resume_file = st.file_uploader(
                "Upload your resume (PDF only)",
                type=["pdf"],
                help="Only PDF files are accepted. Make sure text is selectable in your PDF."
            )
            
            if resume_file:
                st.success(f"✅ Resume uploaded: {resume_file.name}")
                
                # Save file info in session state
                if "resume_file" not in st.session_state or st.session_state.resume_file != resume_file:
                    st.session_state.resume_file = resume_file
                    st.session_state.resume_file_path = save_uploaded_file(resume_file)
                    
                    # Clear previous results if any
                    if "analysis_results" in st.session_state:
                        del st.session_state.analysis_results
                
        with col2:
            st.markdown("""
            <h3 style="color: #424242;">📝 Job Description</h3>
            """, unsafe_allow_html=True)
            
            job_description = st.text_area(
                "Paste the job description here",
                height=200,
                help="Copy and paste the complete job description for accurate analysis",
                key="job_description"
            )
            
            # Save job description in session state
            if "job_description" not in st.session_state or st.session_state.job_description != job_description:
                st.session_state.job_description = job_description
                
                # Clear previous results if any
                if "analysis_results" in st.session_state:
                    del st.session_state.analysis_results
        
        # Center the analyze button
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            analyze_btn = st.button(
                "🔍 Analyze Resume",
                help="Click to analyze how well your resume matches the job description",
                use_container_width=True,
                type="primary"
            )
            
            # Initialize the session state for results if not exists
            if "analysis_results" not in st.session_state:
                st.session_state.analysis_results = None
        
        # Return values needed by the calling function
        return resume_file, job_description, analyze_btn
        
    except Exception as e:
        logger.error(f"Error in input section: {str(e)}")
        raise CustomException(e)


def display_results(results):
    """
    Display the analysis results in an organized, user-friendly format.
    
    Args:
        results: The analysis results from the resume_analyzer function
    """
    try:
        if not results:
            return
            
        # st.markdown("<hr style='margin: 30px 0; border: 0; border-top: 1px solid #ddd;'>", unsafe_allow_html=True)
        
        # st.markdown("""
        # <h2 style="text-align: center; color: #424242;">🎯 Analysis Results</h2>
        # """, unsafe_allow_html=True)
        
        # # Display the match score prominently
        # match_score = results.get("match_score", 0)
        
        # st.markdown(f"""
        # <div style="text-align: center; margin: 20px 0;">
        #     <h1 style="font-size: 3rem; margin-bottom: 0px;">{match_score}%</h1>
        #     <p style="color: #757575; margin-top: 0px;">Resume match score</p>
        # </div>
        # """, unsafe_allow_html=True)
        
        # # Create tabs for different sections of results
        # tab1, tab2, tab3 = st.tabs(["📊 Summary", "🔑 Keywords", "💡 Recommendations"])
        
        # with tab1:
        #     st.markdown("""
        #     <h3 style="color: #424242;">Analysis Summary</h3>
        #     """, unsafe_allow_html=True)
            
        #     # Create columns for the summary stats
        #     col1, col2, col3 = st.columns(3)
            
        #     with col1:
        #         st.metric("Matched Keywords", results.get("matched_keywords_count", 0))
                
        #     with col2:
        #         st.metric("Missing Keywords", results.get("missing_keywords_count", 0))
                
        #     with col3:
        #         st.metric("Total Keywords", results.get("total_keywords_count", 0))
                
        #     # Display summary text
        #     st.markdown(results.get("summary", ""))
        
        # with tab2:
        #     # Create columns for matched vs missing keywords
        #     col1, col2 = st.columns(2)
            
        #     with col1:
        #         st.markdown("""
        #         <h3 style="color: #4CAF50;">✅ Matched Keywords</h3>
        #         """, unsafe_allow_html=True)
                
        #         matched_keywords = results.get("matched_keywords", [])
                
        #         if matched_keywords:
        #             for keyword in matched_keywords:
        #                 st.markdown(f"- **{keyword}**")
        #         else:
        #             st.info("No matched keywords found.")
            
        #     with col2:
        #         st.markdown("""
        #         <h3 style="color: #F44336;">❌ Missing Keywords</h3>
        #         """, unsafe_allow_html=True)
                
        #         missing_keywords = results.get("missing_keywords", [])
                
        #         if missing_keywords:
        #             for keyword in missing_keywords:
        #                 st.markdown(f"- **{keyword}**")
        #         else:
        #             st.success("No missing keywords - great job!")
        
        # with tab3:
        #     st.markdown("""
        #     <h3 style="color: #424242;">Recommendations</h3>
        #     """, unsafe_allow_html=True)
            
        #     recommendations = results.get("recommendations", [])
            
        #     if recommendations:
        #         for i, rec in enumerate(recommendations, 1):
        #             st.markdown(f"### {i}. {rec.get('title', 'Recommendation')}")
        #             st.markdown(rec.get("description", ""))
                    
        #             if "action_items" in rec:
        #                 st.markdown("**Action Items:**")
        #                 for item in rec["action_items"]:
        #                     st.markdown(f"- {item}")
        #     else:
        #         st.info("No specific recommendations available.")
        
        # Add download button for detailed report if available
        st.markdown(results)
            
        logger.debug("Results displayed successfully")
        
    except Exception as e:
        logger.error(f"Error displaying results: {str(e)}")
        st.error("Error displaying results. Please try again.")


def display_footer():
    """Display the footer section with additional information."""
    try:
        st.markdown("<hr style='margin: 30px 0; border: 0; border-top: 1px solid #ddd;'>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; padding: 10px; color: #757575; font-size: 0.8em;">
            <p>ATS Resume Checker Tool • Optimize your resume for Applicant Tracking Systems</p>
            <p>This tool helps you analyze your resume against job descriptions but doesn't guarantee job placement.</p>
        </div>
        """, unsafe_allow_html=True)
        
        logger.debug("Footer displayed")
    except Exception as e:
        logger.error(f"Error displaying footer: {str(e)}")


def ats_checker():
    """Main function for the ATS Checker page."""
    try:
        logger.info("Initializing ATS Checker page")
        
        # Set up page
        page_setup()
        
        # Display sidebar with help information
        display_sidebar()
        
        # Display header
        display_header()
        
        # Display input section and get user inputs
        resume_file, job_description, analyze_btn = display_input_section()
    
        # Process analysis if the button is clicked
        if analyze_btn:
            if resume_file is None:
                st.error("Please upload your resume first.")
                logger.warning("Analysis attempted without resume upload")
                return
                
            if not job_description.strip():
                st.error("Please paste the job description.")
                logger.warning("Analysis attempted without job description")
                return
                
            try:
                # Show processing animation
                with st.spinner("Analyzing your resume against the job description..."):
                    # Artificial delay to show progress bar

                    
                    # Get resume file path from session state

                    
                    # Perform the analysis
                    progress_bar = st.progress(5)
                    results = resume_analyzer(resume_file, job_description)
                    for i in range(100):

                        time.sleep(0.05)
                        progress_bar.progress(i + 1)

                    
                    # Store results in session state
                    st.session_state.analysis_results = results
                    
                # Remove progress bar after completion
                progress_bar.empty()
                
                if results:
                    st.success("Analysis complete! View your results below.")
                    logger.info("Resume analysis completed successfully")
                else:
                    st.error("Failed to analyze resume. Please try again.")
                    logger.error("Resume analysis returned no results")
                    
            except CustomException as ce:
                st.error(f"Error: {str(ce)}")
                logger.error(f"Custom error during resume analysis: {str(ce)}")
            except Exception as e:
                st.error("An unexpected error occurred. Please try again later.")
                logger.error(f"Unexpected error in resume analysis: {str(e)}")
        
        # Display results if available in session state
        if "analysis_results" in st.session_state and st.session_state.analysis_results:
            display_results(st.session_state.analysis_results)
        
        # Display footer
        display_footer()
        
    except Exception as e:
        logger.critical(f"Unexpected error in ATS Checker page: {str(e)}")
        st.error("A system error occurred. Please refresh the page and try again.")
        raise CustomException(e)


if __name__ == "__main__":
    ats_checker()