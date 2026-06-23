import contextlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.session import SessionLocal, engine
from app.models.base import Base
from app.models.user import UserRole
from app.routes.api import api_router
from app.schemas.user import UserCreate
from app.services.user_service import get_user_by_email, create_user


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler that manages application startup and shutdown.
    Creates tables and seeds the initial admin user automatically.
    """
    # 1. Automatically create database tables if they do not exist
    # (Acts as a fallback if Alembic is not executed first)
    Base.metadata.create_all(bind=engine)
    
    # 2. Seed default admin superuser
    db = SessionLocal()
    try:
        admin_email = settings.FIRST_SUPERUSER_EMAIL
        if admin_email:
            admin = get_user_by_email(db, email=admin_email)
            if not admin:
                user_in = UserCreate(
                    email=admin_email,
                    full_name="Platform Administrator",
                    password=settings.FIRST_SUPERUSER_PASSWORD,
                    role=UserRole.ADMIN,
                    phone="+213555000000",
                )
                create_user(db=db, user_in=user_in)
                print(f"Successfully seeded superuser: {admin_email}")
    except Exception as e:
        print(f"Error seeding initial superuser: {e}")
    finally:
        db.close()
        
    yield  # Application runs here
    
    # Shutdown logic (if any) goes here


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description=(
        "FastAPI Backend for SkillUp, an Algerian platform that connects "
        "young people with skilled craftsmen and professionals to gain "
        "practical experience."
    ),
    lifespan=lifespan,
)

# Set up CORS (Cross-Origin Resource Sharing) middleware
# Allowing all origins in development; restrict this in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include main router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Serve frontend static files (index.html, assets, pages) so the same server
# can serve the SPA and the API. Keep API under the `/api/v1` prefix.
from fastapi.staticfiles import StaticFiles

# Mount the project root as static so `index.html` is served at `/`.
app.mount("/", StaticFiles(directory=".", html=True), name="static")


@app.get("/", tags=["Root"])
def root():
    """
    Root status endpoint.
    """
    return {
        "status": "online",
        "message": f"Welcome to the {settings.PROJECT_NAME}!",
        "documentation": "/docs",
    }
