import streamlit as st

from app.utils.api_clients.job_posting_analyser_client import analyze_job_posting


def job_posting_analyser():
    try:
        url = st.text_input("Enter the job posting url", placeholder="https://example.com")
        if st.button("Analyze"):
            if url:
                with st.spinner("Analyzing..."):
                    response = analyze_job_posting(url)
                    st.markdown(response)
    except Exception as e:
            st.error(f"Error processing response: {e}")