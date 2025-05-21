import streamlit as st
from app.core.logger import get_logger
# from app.components.resume_tailor.html_populator import process_resume_data
from app.components.resume_tailor.html_to_pdf import create_pdf_from_html
from app.utils.api_clients.resume_tailor_client import tailor_resume_and_guide

logger = get_logger(__name__)

def resume_builder():
    """Main function to render the resume builder UI"""

    # Set up session state to persist data after form submission
    if "submitted" not in st.session_state:
        st.session_state.submitted = False
        # st.session_state.resume_json = None
        st.session_state.markdown_result = ""
        st.session_state.pdf_bytes = None

    # === Form Inputs ===
    with st.form("resume_form"):
        resume_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
        job_posting_link = st.text_input("Paste the job posting link")
        github_link = st.text_input("Paste GitHub link")
        write_up = st.text_area("Write your personal statement")
        submit_button = st.form_submit_button("Analyze")

    # === If Form Submitted ===
    if submit_button:
        if not all([job_posting_link, github_link, write_up]):
            st.warning("Please fill out all fields")
            return

        with st.spinner("Analyzing your resume and job posting..."):
            try:
                response = tailor_resume_and_guide(resume_file, job_posting_link, github_link, write_up)

                # resume_json = response.get("resume_json")
                markdown_result = response.get("result", "No analysis provided.")

                # if not resume_json:
                #     st.error("Invalid response format: missing resume data")
                #     return

                # Generate HTML & PDF
                # html_content = process_resume_data(resume_json)
                output_pdf_path = "data/resume_templates/tailored_resume.pdf"
                pdf_bytes = create_pdf_from_html(output_pdf_path)

                # Save results to session
                st.session_state.submitted = True
                # st.session_state.resume_json = resume_json
                st.session_state.markdown_result = markdown_result
                st.session_state.pdf_bytes = pdf_bytes

                st.success("Your tailored resume is ready!")

            except Exception as e:
                logger.exception(f"Error generating resume: {str(e)}")
                st.error(f"Something went wrong. Please try again.{e}")

    # === Display Results and Download Button AFTER Submission ===
    if st.session_state.submitted:
        st.download_button(
            label="Download Tailored Resume",
            data=st.session_state.pdf_bytes,
            file_name="tailored_resume.pdf",
            mime="application/pdf"
        )

        st.subheader("Resume Analysis")
        st.markdown(st.session_state.markdown_result)
