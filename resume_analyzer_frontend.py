import streamlit as st
import requests

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
                # Prepare the files and data for the POST request
                files = {"file": uploaded_file.getvalue()}
                payload = {"job_description": job_description}  # Send job_description as form-data
                
                # Send the POST request to FastAPI server
                response = requests.post("http://localhost:8000/analyze/", files=files, data=payload)
                
                # Check if the response is successful
                if response.status_code == 200:
                    result = response.json()
                    extracted_data = result["parsed_resume"]
                    analysis_result = result["analysis_result"]
                    
                    # Display Extracted Data
                    st.subheader("Extracted Resume Details")
                    st.write(f"**Name:** {extracted_data.get('name', 'N/A')}")
                    st.write(f"**Email:** {extracted_data.get('email', 'N/A')}")
                    st.write(f"**Skills:** {', '.join(extracted_data.get('skills', []))}")
                    st.write(f"**Education:** {extracted_data.get('education', 'N/A')}")
                    
                    # Display Analysis Result
                    st.subheader("Resume Analysis")
                    st.write(analysis_result)
                else:
                    st.error("Error analyzing resume. Please try again.")

if __name__ == "__main__":
    main()
