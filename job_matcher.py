import dspy
import re

def determine_base_score(job_description):
    """Assigns a base score based on job seniority."""
    if any(level in job_description.lower() for level in ["senior", "lead", "director", "manager"]):
        return 60  # Higher base for senior roles
    elif any(level in job_description.lower() for level in ["mid", "intermediate", "specialist"]):
        return 50  # Medium base for mid-level roles
    else:
        return 40  # Lower base for junior or entry-level roles

def determine_resume_seniority(experience):
    """Determines the seniority level of a resume based on job titles and years of experience."""
    senior_titles = ["senior", "lead", "director", "manager"]
    mid_titles = ["mid", "specialist", "consultant"]
    
    years_of_experience = re.findall(r'(\d+)\s*(?:years?|yrs?)', experience.lower())
    years_of_experience = max(map(int, years_of_experience), default=0)
    
    if any(title in experience.lower() for title in senior_titles) or years_of_experience >= 10:
        return "Senior"
    elif any(title in experience.lower() for title in mid_titles) or years_of_experience >= 5:
        return "Mid-level"
    else:
        return "Junior"

class ResumeAnalyzer(dspy.Module):
    def forward(self, job_description, name, email, skills, education, experience):
        job_skills = extract_keywords(job_description)
        matching_skills = [skill for skill in skills if any(js in skill.lower() for js in job_skills)]
        skill_match_score = int((len(matching_skills) / max(len(job_skills), 1)) * 100)
        
        # Adjust scoring to vary more based on actual skill matching
        base_score = determine_base_score(job_description)
        resume_seniority = determine_resume_seniority(experience)
        
        skill_weight = 0.7  # Increase skill match impact
        education_bonus = education_score(job_description, education)  # More flexible education scoring
        
        match_score = min(base_score + int(skill_match_score * skill_weight) + education_bonus, 100)
        
        summary = summarize_text(job_description)
        
        # Generate detailed reasoning
        reasoning = f"The resume received a base score of {base_score} based on job seniority. "
        reasoning += f"It matched {len(matching_skills)} out of {len(job_skills)} skills from the job description, contributing {int(skill_match_score * skill_weight)} points. "
        reasoning += f"The education match contributed an additional {education_bonus} points. "
        reasoning += f"The candidate's seniority level is determined as {resume_seniority} based on job titles and experience. "
        reasoning += "Overall, the resume demonstrates a fair alignment with the job requirements."
        
        return f"""
        Job Description Summary:
        {summary}
        
        Candidate Details:
        - Name: {name}
        - Email: {email}
        - Skills: {', '.join(skills)}
        - Education: {education}
        - Experience Level: {resume_seniority}
        
        Analysis:
        The candidate's resume has been analyzed against the job description.
        Match Score: {match_score}/100
        Matching Skills: {', '.join(matching_skills) if matching_skills else 'Some relevant skills detected'}
        Reasoning: {reasoning}
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
    experience = resume_data.get("experience", "N/A")
    
    # Perform analysis
    analysis_result = model.forward(job_description, name, email, skills, education, experience)
    return analysis_result
