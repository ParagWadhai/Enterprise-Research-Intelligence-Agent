from fastapi import FastAPI

from app.api.research import router as research_router

from app.database.database import (
    Base,
    engine,
)

# IMPORTANT:
# Import models so SQLAlchemy knows about all tables
# before create_all() runs.
from app.database import models


app = FastAPI(
    title="Enterprise Research Intelligence Agent",
    description=(
        "AI-powered enterprise research and intelligence platform"
    ),
    version="1.0.0",
)


# ---------------------------------------------------------
# Database initialization
# ---------------------------------------------------------

@app.on_event("startup")
def startup():

    Base.metadata.create_all(
        bind=engine
    )


# ---------------------------------------------------------
# Routers
# ---------------------------------------------------------

app.include_router(
    research_router
)


# ---------------------------------------------------------
# Root
# ---------------------------------------------------------

@app.get("/")
def root():

    return {
        "application": (
            "Enterprise Research Intelligence Agent"
        ),
        "status": "running",
        "version": "1.0.0",
    }


# ---------------------------------------------------------
# Health
# ---------------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }