from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import notifications
from .database import engine
from . import models

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Notification Service API",
    description="Microservice for sending notifications (emails, etc.) working Online!",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(notifications.router)

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "notification-service"}

@app.get("/")
def root():
    return {
        "message": "Welcome to Notification Service",
        "endpoints": {
            "docs": "/api/docs",
            "send_notification": "/notifications/send",
            "notifications": "/notifications"
        }
    }

