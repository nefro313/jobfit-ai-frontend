"""
Job Posting Analyzer UI Module

This module provides a Streamlit-based user interface for the job posting analyzer
feature, allowing users to enter job URLs and view analysis results.
"""

import streamlit as st


from urllib.parse import urlparse

# Import custom modules
from app.utils.api_clients.job_posting_analyser_client import analyze_job_posting
from app.core.exceptions import CustomException
from app.core.logger import get_logger

# Initialize logger for this module
logger = get_logger(__name__)


def is_valid_url(url: str) -> bool:
    """
    Validate if the provided string is a properly formatted URL.
    
    Args:
        url (str): The URL string to validate
        
    Returns:
        bool: True if the URL is valid, False otherwise
    """
    if not url:
        return False
        
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception as e:
        logger.warning(f"URL validation error: {str(e)}")
        return False


def display_job_posting_analyzer():
    """
    Display the job posting analyzer interface in Streamlit.
    
    This function creates a user interface with:
    - Title and description
    - URL input field
    - Analysis button
    - Results display area
    - Error handling for invalid inputs or API errors
    """
    logger.info("Loading job posting analyzer UI")
    
    # Set page configuration
    st.set_page_config(
        page_title="Job Posting Analyzer",
        page_icon="📋",
        layout="wide"
    )
    
    # UI Header
    st.title("📋 Job Posting Analyzer")
    st.markdown("""
    Analyze job postings to understand key requirements and how well your resume matches.
    Enter a job posting URL below to get started.
    """)
    
    # Create two columns for the URL input and analyze button
    col1, col2 = st.columns([3, 1])
    
    with col1:
        url = st.text_input(
            "Job posting URL",
            placeholder="https://example.com/job-posting",
            help="Enter the full URL of the job posting you want to analyze"
        )
    
    with col2:
        st.write("")  # Add some spacing
        st.write("")  # Add some spacing
        analyze_button = st.button("Analyze Job", type="primary", use_container_width=True)
    
    # Remember the analysis results in session state
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None
        
    # Process the URL when the analyze button is clicked
    if analyze_button:
        if not url:
            st.error("Please enter a job posting URL")
            logger.warning("User attempted analysis without entering a URL")
        elif not is_valid_url(url):
            st.error("Please enter a valid URL (e.g., https://example.com/job)")
            logger.warning(f"User entered invalid URL: {url}")
        else:
            try:
                # Show a spinner while analyzing
                with st.spinner("Analyzing job posting..."):
                    logger.info(f"Analyzing job posting URL: {url}")
                    analysis_results = analyze_job_posting(url)
                    st.session_state.analysis_results = analysis_results
                    
                if analysis_results:
                    logger.info("Successfully retrieved analysis results")
                else:
                    st.error("Failed to analyze the job posting. Please try again later.")
                    logger.error(f"API returned no results for URL: {url}")
            
            except CustomException as ce:
                st.error(f"Error: {str(ce)}")
                logger.error(f"Custom error during job analysis: {str(ce)}")
            except Exception as e:
                st.error("An unexpected error occurred. Please try again later.")
                logger.error(f"Unexpected error in job analysis UI: {str(e)}")
    
    # Display analysis results if available
    if st.session_state.analysis_results:
        st.success("Analysis completed successfully!")
        
        # Create tabs for different sections of the analysis
        # tab1, tab2, tab3 = st.tabs(["Summary", "Key Requirements", "Recommendations"])
        
        # with tab1:
        #     st.subheader("Job Posting Analysis")
        #     st.markdown(st.session_state.analysis_results.get("summary", "No summary available"))
            
        # with tab2:
        #     st.subheader("Key Requirements")
        #     requirements = st.session_state.analysis_results.get("requirements", [])
            
        #     if requirements:
        #         for category, items in requirements.items():
        #             with st.expander(f"{category} ({len(items)})", expanded=True):
        #                 for item in items:
        #                     st.markdown(f"- {item}")
        #     else:
        #         st.info("No specific requirements identified")
                
        # with tab3:
        #     st.subheader("Recommendations")
        #     recommendations = st.session_state.analysis_results.get("recommendations", [])
            
        #     if recommendations:
        #         for rec in recommendations:
        #             st.markdown(f"- {rec}")
        #     else:
        #         st.info("No specific recommendations available")
        st.markdown(st.session_state.analysis_results)
        
    
    # Add footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: gray; font-size: 0.8em;">
        Job Posting Analyzer Tool • Helping you understand job requirements better
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    try:
        logger.info("Starting Job Posting Analyzer application")
        display_job_posting_analyzer()
    except Exception as e:
        logger.critical(f"Application crashed: {str(e)}")
        st.error("The application encountered a critical error. Please refresh the page or try again later.")