from fastapi import FastAPI
from app.routers.routes import routes

app = FastAPI(
    title="FastAPI Auth",
    description="This API handles user management and Auth",
    version="1.0.0"
    )

# Include routers
app.include_router(routes, prefix="/v1")

# Root route
@app.get("/")
def read_root():
    return {"message": "M29 doesn't share code!"}

# Health check route
@app.get("/health")
def health_check():
    return {"status": "Running..."}
