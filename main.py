from fastapi import FastAPI, UploadFile, File, Form
from resume_parser import parse_resume
from job_matcher import analyze_resume
import uvicorn

app = FastAPI()

@app.post("/analyze/")
async def analyze_resume_api(job_description: str = Form(...), file: UploadFile = File(...)):
    """API endpoint to analyze a resume against a job description."""
    print(f"Received job_description: {job_description}")  # Debugging line
    parsed_resume = parse_resume(file.file)
    analysis_result = analyze_resume(parsed_resume, job_description)
    return {"parsed_resume": parsed_resume, "analysis_result": analysis_result}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
