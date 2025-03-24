import dspy

class ResumeAnalyzer(dspy.Module):
    def forward(self, job_description, name, email, skills, education):
        return f"""
        Job Description:
        {job_description}
        
        Candidate Details:
        - Name: {name}
        - Email: {email}
        - Skills: {', '.join(skills)}
        - Education: {education}
        
        Analyze how well this candidate matches the job description and provide a match score (0-100) with reasoning.
        """

def analyze_resume(resume_data, job_description):
    """Analyzes the resume against the job description using DSPy."""
    model = ResumeAnalyzer()
    
    # Extract structured resume details
    name = resume_data.get("name", "N/A")
    email = resume_data.get("email", "N/A")
    skills = resume_data.get("skills", [])
    education = resume_data.get("education", "N/A")
    
    # Perform analysis
    analysis_result = model.forward(job_description, name, email, skills, education)
    return analysis_result
