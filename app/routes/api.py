from fastapi import APIRouter
from app.routes import auth, users, skills, trainer_profiles, training_requests, reviews

api_router = APIRouter()

# Include all sub-routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(skills.router, prefix="/skills", tags=["Skills"])
api_router.include_router(
    trainer_profiles.router, prefix="/trainers", tags=["Trainer Profiles"]
)
api_router.include_router(
    training_requests.router, prefix="/requests", tags=["Training Requests"]
)
api_router.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])
