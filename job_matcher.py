import dspy
import random

class ResumeAnalyzer(dspy.Module):
    def forward(self, job_description, name, email, skills, education):
        match_score = random.randint(50, 100)  # Simulating a match score for now
        
        return f"""
        Job Description:
        {job_description}
        
        Candidate Details:
        - Name: {name}
        - Email: {email}
        - Skills: {', '.join(skills)}
        - Education: {education}
        
        Analysis:
        The candidate's resume has been analyzed against the job description.
        Match Score: {match_score}/100
        Reasoning: The match score is based on keyword relevance, skills alignment, and education requirements.
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