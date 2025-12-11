# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.endpoint.material_router import material_router
# from app.settings import settings

# app = FastAPI(
#     title="Materials Service",
#     description="Microservice for managing educational materials",
#     version="1.0.0"
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(material_router, prefix="/api")

# @app.get("/")
# async def root():
#     return {"message": "Materials Service API", "status": "running"}

# @app.get("/health")
# async def health_check():
#     return {"status": "healthy", "service": "materials"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(
#         "app.main:app",
#         host=settings.host,
#         port=settings.port,
#         reload=True
#     )


from fastapi import FastAPI
from .routers import materials
from .database import engine
from . import models

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Materials Service API",
    description="Microservice for managing educational materials",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Include routers
app.include_router(materials.router)

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "materials-service"}

@app.get("/")
def root():
    return {
        "message": "Welcome to Materials Service",
        "endpoints": {
            "docs": "/api/docs",
            "materials": "/materials"
        }
    }
# docker-compose start to start and stop the container, 