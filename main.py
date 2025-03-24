import streamlit as st
from resume_parser import parse_resume
from job_matcher import analyze_resume

def main():
    st.title("Resume Analyzer")
    
    # Job Description Input
    st.subheader("Job Description")
    job_description = st.text_area("Enter the job description")
    
    # Resume Upload
    st.subheader("Upload Resume")
    uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
    
    if uploaded_file and job_description:
        if st.button("Analyze Resume"):
            with st.spinner("Processing..."):
                extracted_data = parse_resume(uploaded_file)
                analysis_result = analyze_resume(extracted_data, job_description)
                
                # Display Extracted Data
                st.subheader("Extracted Resume Details")
                st.write(f"**Name:** {extracted_data.get('name', 'N/A')}")
                st.write(f"**Email:** {extracted_data.get('email', 'N/A')}")
                st.write(f"**Skills:** {', '.join(extracted_data.get('skills', []))}")
                st.write(f"**Education:** {extracted_data.get('education', 'N/A')}")
                
                # Display Analysis Result
                st.subheader("Resume Analysis")
                st.write(analysis_result)
    
if __name__ == "__main__":
    main()
