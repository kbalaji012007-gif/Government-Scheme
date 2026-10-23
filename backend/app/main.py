import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.db.firebase import db_manager
from app.routers import health, categories, schemes, centers, auth

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("ruralconnect.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to DB and auto-seed if empty
    logger.info("Initializing RuralConnect Karnataka backend services...")
    db_manager.connect()
    
    # Try seeding sample data if schemes collection is empty
    try:
        from scripts.seed_data import seed_database
        seed_database(auto_if_empty=True)
    except Exception as exc:
        logger.warning("Auto-seed notice: %s", exc)

    yield

    # Shutdown: Cleanly close DB connection
    logger.info("Shutting down RuralConnect Karnataka backend services...")
    db_manager.disconnect()


app = FastAPI(
    title="RuralConnect Karnataka API",
    description=(
        "Public welfare scheme discovery and accessibility platform for rural Karnataka. "
        "Disclaimer: This service provides preliminary eligibility discovery guidance and "
        "is not an official government approval authority."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
origins = settings.cors_origins
logger.info("Configuring CORS for origins: %s", origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Clean validation error formatting without leaking stack traces."""
    errors = []
    for err in exc.errors():
        loc = " -> ".join([str(l) for l in err.get("loc", [])])
        msg = err.get("msg", "Invalid value")
        errors.append(f"{loc}: {msg}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Request validation failed",
            "errors": errors,
        },
    )


# Register API v1 Routers
api_v1_prefix = "/api/v1"
app.include_router(health.router, prefix=api_v1_prefix)
app.include_router(categories.router, prefix=api_v1_prefix)
app.include_router(schemes.router, prefix=api_v1_prefix)
app.include_router(centers.router, prefix=api_v1_prefix)
app.include_router(auth.router, prefix=api_v1_prefix)


@app.get("/", tags=["Root"])
async def root():
    return {
        "name": "RuralConnect Karnataka API",
        "description": "Discover government schemes, understand eligibility, and find the support you need.",
        "documentation": "/docs",
        "health": "/api/v1/health",
        "disclaimer": "Informational discovery platform. Not an official government endorsement.",
    }
