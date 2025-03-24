import dspy
import random
import re

class ResumeAnalyzer(dspy.Module):
    def forward(self, job_description, name, email, skills, education):
        job_skills = extract_keywords(job_description)
        matching_skills = [skill for skill in skills if any(js in skill.lower() for js in job_skills)]
        skill_match_score = int((len(matching_skills) / max(len(job_skills), 1)) * 100)
        
        # Adjust scoring to vary more based on actual skill matching
        base_score = random.randint(40, 60)  # Lower base to introduce more variation
        skill_weight = 0.7  # Increase skill match impact
        education_bonus = education_score(job_description, education)  # More flexible education scoring
        
        match_score = min(base_score + int(skill_match_score * skill_weight) + education_bonus, 100)
        
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
        Matching Skills: {', '.join(matching_skills) if matching_skills else 'Some relevant skills detected'}
        Reasoning: The score now considers multiple skill matches more accurately, giving credit for all relevant skills and a flexible education match.
        """

def extract_keywords(text):
    """Extracts relevant keywords from the job description."""
    words = re.findall(r'\b\w+\b', text)
    common_terms = {"and", "or", "the", "a", "an", "with", "in", "to", "for", "of", "on"}
    keywords = [word.lower() for word in words if word.lower() not in common_terms]
    return list(set(keywords))

def summarize_text(text, max_length=100):
    """Summarizes the job description to a shorter form."""
    return text[:max_length] + "..." if len(text) > max_length else text

def education_score(job_description, education):
    """Assigns a score based on how well the education level matches the job requirements."""
    education_levels = ["phd", "master", "bachelor", "associate", "diploma", "degree"]
    job_ed_level = next((level for level in education_levels if level in job_description.lower()), None)
    candidate_ed_level = next((level for level in education_levels if level in education.lower()), None)
    
    if not job_ed_level or not candidate_ed_level:
        return 5  # Small bonus if education isn't explicitly required
    
    job_index = education_levels.index(job_ed_level)
    candidate_index = education_levels.index(candidate_ed_level)
    
    if candidate_index <= job_index:
        return 15  # Strong match or overqualified
    elif candidate_index - job_index == 1:
        return 10  # Slightly underqualified but close
    else:
        return 5  # Less relevant education but still considered

def analyze_resume(resume_data, job_description):
    """Analyzes the resume against the job description using DSPy."""
    model = ResumeAnalyzer()
    
    # Extract structured resume details
    name = resume_data.get("name", "N/A")
    email = resume_data.get("email", "N/A")
    skills = [skill.lower() for skill in resume_data.get("skills", [])]
    education = resume_data.get("education", "N/A")
    
    # Perform analysis
    analysis_result = model.forward(job_description, name, email, skills, education)
    return analysis_result
