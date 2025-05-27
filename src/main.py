from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import companies, jobs, applications  # imported the applications router here

app = FastAPI(title="Job Board API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(companies.router, prefix="/companies", tags=["companies"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(applications.router)  # included the applications router here

@app.get("/")
def read_root():
    return {"message": "Welcome to the Job Board API"}





