from fastapi import FastAPI

app = FastAPI(title="TestPilot")


@app.get("/")
def root():
    return {"message": "TestPilot API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
