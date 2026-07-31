from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Railway Working"}

@app.get("/health")
def health():
    return {"status": "healthy"}
