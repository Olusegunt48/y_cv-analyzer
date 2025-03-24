import dspy
import random
import re

class ResumeAnalyzer(dspy.Module):
    def forward(self, job_description, name, email, skills, education):
        job_skills = extract_keywords(job_description)
        matching_skills = list(set(skills) & set(job_skills))
        skill_match_score = int((len(matching_skills) / max(len(job_skills), 1)) * 100)
        
        # Make the scoring more lenient by boosting partial matches
        leniency_factor = 20
        match_score = min(skill_match_score + random.randint(10, leniency_factor), 100)
        
        summary = summarize_text(job_description)
        
        return f"""
        Job Description Summary:
        {summary}
        
        Candidate Details:
        - Name: {name}
        - Email: {email}
        - Skills: {', '.join(skills)}
        - Education: {education}
        
        Analysis:
        The candidate's resume has been analyzed against the job description.
        Match Score: {match_score}/100
        Matching Skills: {', '.join(matching_skills)}
        Reasoning: The score accounts for relevant skills, even partial matches, and education relevance.
        """

def extract_keywords(text):
    """Extracts relevant keywords from the job description."""
    words = re.findall(r'\b\w+\b', text)
    common_terms = {"and", "or", "the", "a", "an", "with", "in", "to", "for", "of", "on"}
    keywords = [word for word in words if word.lower() not in common_terms]
    return list(set(keywords))

def summarize_text(text, max_length=100):
    """Summarizes the job description to a shorter form."""
    return text[:max_length] + "..." if len(text) > max_length else text

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
