import streamlit as st
from app.utils.api_clients.hr_qa_client import hr_qa_client

def hr_behavioral_qa():
    """HR Behavioral Interview QA Interface with enhanced UX"""
    
    # Configure page layout
    st.set_page_config(page_title="HR Behavioral Assistant", layout="wide")
    
    with st.container():
        st.markdown("""
            # HR Behavioral Assessment Assistant
            **Get HR answer** to behavioral interview questions
        """)
        
        # Help section with examples
        with st.expander("💡 Example Behavioral Questions"):
            st.markdown("""
                Common behavioral patterns to analyze:
                - *Conflict Resolution*: "Tell me about a time you disagreed with a team member"
                - *Leadership*: "Describe a situation where you had to lead without formal authority"
                - *Adaptability*: "Give an example of when you had to quickly learn something new"
            """)
        
        # Input section
        col1, col2 = st.columns([4, 1])
        with col1:
            query = st.text_area(
                "Enter Behavioral Question :",
                placeholder="Enter the Your question.",
            )
        
        with col2:
            st.markdown("<div style='height: 38px'></div>", unsafe_allow_html=True)
            analyze_btn = st.button("🔍 Analyze Response", use_container_width=True)

        if analyze_btn:
            if not query:
                st.warning("⚠️ Please input the qurey")
                st.stop()
                
            with st.status("🧠 Analyzing behavioral patterns...", expanded=True) as status:
                try:
                    answer = hr_qa_client(query)
                    if not answer:
                        raise ValueError("Empty response from analysis engine")
                        
                    status.update(label="Analysis Complete!", state="complete") 
                    st.toast("✅ Analysis generated!", icon="✅")
                    
                    with st.container(border=True):
                        st.markdown("""
                            ## Behavioral Assessment Result
                            *Key insights from the candidate's response:*
                        """)
                        st.divider()
                        st.markdown(answer)  # Direct Markdown rendering
                        
                except Exception as e:
                    status.update(label="Analysis Failed", state="error")
                    st.error(f"""
                        ❌ Failed to analyze response:
                        **Error:** {str(e)}
                        Please try again or check the input format
                    """)

if __name__ == "__main__":
    hr_behavioral_qa()