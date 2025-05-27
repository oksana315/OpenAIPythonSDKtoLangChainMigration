from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models import models
from app.schemas import schemas

from app.schemas.schemas import JobDescriptionRequest, JobDescriptionResponse
from app.models.models import JobPosting, Company  # Assuming Company model exists
from openai import OpenAI
import datetime, os

router = APIRouter()

client = OpenAI()

#/jobs
# {  company_id: 1
#    title: "Sr. AI Engineer"
#    "compensation_min": 200000
#    compensation_max: 300000
#    location_type: REMOTE
##    employment_type: FULLTIME
 #     "workAuthStatus": H1B
#   }
#
#
#/jobs
@router.post("/", response_model=schemas.JobPosting)
def create_job_posting(job: schemas.JobPostingCreate, db: Session = Depends(get_db)):
    # Verify company exists
    company = db.query(models.Company).filter(models.Company.id == job.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db_job = models.JobPosting(**job.model_dump()) #create a JobPosting Object with default values (**job.model_dump()) just pass all the required constructor values
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/", response_model=List[schemas.JobPosting])
def read_job_postings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = db.query(models.JobPosting).offset(skip).limit(limit).all()
    return jobs

#jobs/6
@router.get("/{job_id}", response_model=schemas.JobPosting)
def read_job_posting(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(models.JobPosting).filter(models.JobPosting.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job posting not found")
    return db_job

@router.put("/{job_id}", response_model=schemas.JobPosting)
def update_job_posting(job_id: int, job: schemas.JobPostingUpdate, db: Session = Depends(get_db)):
    db_job = db.query(models.JobPosting).filter(models.JobPosting.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job posting not found")
    
    # If company_id is being updated, verify the new company exists
    if job.company_id is not None:
        company = db.query(models.Company).filter(models.Company.id == job.company_id).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
    
    update_data = job.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_job, field, value)
    
    db.commit()
    db.refresh(db_job)
    return db_job

@router.delete("/{job_id}")
def delete_job_posting(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(models.JobPosting).filter(models.JobPosting.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job posting not found")
    
    db.delete(db_job)
    db.commit()
    return {"message": "Job posting deleted successfully"} 




#Homework 

@router.post("/{job_id}/description", response_model=schemas.JobDescriptionResponse)
async def generate_job_description(
    job_id: int,
    req: schemas.JobDescriptionRequest,
    db: Session = Depends(get_db)
):
    # 1. Fetch job posting & company from DB
    job = db.query(models.JobPosting).filter(models.JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job posting not found")
    
    company = db.query(models.Company).filter(models.Company.id == job.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    # 2. Build prompt for GPT
    required_tools_str = ", ".join(req.required_tools)
    prompt = (
        f"Write a detailed job description for the following position:\n"
        f"Company: {company.name}\n"              #\n - is a new line
        f"Job Title: {job.title}\n"
        f"Required Tools: {required_tools_str}\n"
        f"Include responsibilities and qualifications."
    )

    # 3. Call OpenAI API
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes professional job descriptions."},
            {"role": "user", "content": prompt},
        ]
    )

    description = response.choices[0].message.content.strip()

    # 4. Save description to DB
    job.description = description
    db.commit()
    db.refresh(job)

    # 5. Return response
    return schemas.JobDescriptionResponse(
        job_id=job.id,
        description=description,
        generated_at=datetime.datetime.utcnow()
    )
             