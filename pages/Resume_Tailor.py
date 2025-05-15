import streamlit as st
from app.components.resume_builder import resume_builder

def resume_tailor():
    st.title("AI Resume Tailor")
    st.write("Upload your resume and job details to create a tailored resume")
    resume_builder()

if __name__ == "__main__":
    resume_tailor()
