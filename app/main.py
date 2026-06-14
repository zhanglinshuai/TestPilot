from fastapi import FastAPI

from app.routers import users, projects

app = FastAPI(title="TestPilot")
app.include_router(users.router)
app.include_router(projects.router)

@app.get("/")
def root():
    return {"message": "TestPilot API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok",}
