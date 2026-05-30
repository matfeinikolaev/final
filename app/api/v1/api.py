from fastapi import APIRouter
from app.api.v1.endpoints import auth, jobs, users, resumes, vacancies, categories

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(vacancies.router, prefix="/vacancies", tags=["vacancies"])
api_router.include_router(resumes.router, prefix="/resumes", tags=["resumes"])
