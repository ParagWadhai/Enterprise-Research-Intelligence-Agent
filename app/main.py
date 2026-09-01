from fastapi import FastAPI

print("STEP 1: main.py started", flush=True)

from app.api.research import router as research_router

print("STEP 2: research router imported", flush=True)

from app.database.database import (
    Base,
    engine,
)

print("STEP 3: database imported", flush=True)

from app.database import models

print("STEP 4: models imported", flush=True)

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

    print("STEP 5: startup event", flush=True)

    Base.metadata.create_all(
        bind=engine
    )

    print("STEP 6: database initialized", flush=True)


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