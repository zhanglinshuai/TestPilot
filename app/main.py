from fastapi import FastAPI
from app.config import settings
from app.routers import users
app = FastAPI(title="TestPilot")
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "TestPilot API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok",}
