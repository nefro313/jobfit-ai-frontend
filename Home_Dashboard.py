import streamlit as st
import os
def home_dashboard():
    # Custom CSS styling
    st.markdown("""
    <style>
        .header {background: linear-gradient(45deg, #4B32C3, #0078D4); padding: 2rem; border-radius: 15px;}
        .service-card {padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.2s;}
        .service-card:hover {transform: translateY(-5px);}
        .icon {font-size: 2.5rem; margin-bottom: 1rem;}
        .nav-button {width: 100%; margin-top: 1rem;}
        @media (max-width: 768px) {.service-card {margin-bottom: 1rem;}}
    </style>
    """, unsafe_allow_html=True)

    # Header Section
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("assets/jobfit-logo.png", width=200)
        with col2:
            st.markdown("<div class='header'>", unsafe_allow_html=True)
            st.title("Welcome to JobFit AI Suite 🚀")
            st.markdown("""
            Your all-in-one AI-powered career optimization platform
            """)
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Services Grid
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.header("✨ Core Features", divider="rainbow")
    
    services = [
        {
            "title": "ATS Dashboard",
            "url": "http://localhost:8501/Ats_Dashboard",
            "icon": "📊",
            "desc": "Analyze resume against job descriptions & get ATS optimization tips"
        },
        {
            "title": "HR Q&A Assistant",
            "url": "http://localhost:8501/HR_Question_Answer",
            "icon": "💬",
            "desc": "Prepare for interviews with AI-powered behavioral question answers"
        },
        {
            "title": "Job Post Analyzer",
            "url": "http://localhost:8501/Job_Posting_Analyser",
            "icon": "🔍",
            "desc": "Decode job postings & identify key requirements"
        },
        {
            "title": "Resume Tailor",
            "url": "http://localhost:8501/Resume_Tailor",
            "icon": "✂️",
            "desc": "Create targeted resumes using GitHub, job posts & personal insights"
        }
    ]

    cols = st.columns(4)
    for idx, (col, service) in enumerate(zip(cols, services)):
        with col:
            st.markdown(f"""
            <div class="service-card" style="border: 1px solid #e0e0e0; background: {'#f8f9fa' if idx%2 else 'white'}">
                <div class="icon">{service['icon']}</div>
                <h3>{service['title']}</h3>
                <p style="color: #666; min-height: 80px">{service['desc']}</p>
                <a href="{service['url']}" target="_self">
                    <button class="nav-button">
                        Try {service['title'].split()[0]} →
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 4rem; color: #666">
        <hr>
        <p>Hey do like this project and find it useful!</p>
        <a href="https://buymeacoffee.com/nefero">☕ Why don't you "Buy Me a Coffee"</a>
        <p>🚀 Powered by AI • 🔒 Secure & Private • 🎯 Career Success Optimizer</p>
        <p>Need help? Contact </p>
        <a href="mailto:robinkphilip2001@gmail.com">Write Me Email: robinkphilip2001@gmail.com</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    home_dashboard()
    os.system("playwright install")
    os.system("playwright install-deps")