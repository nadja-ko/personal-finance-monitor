from fastapi import FastAPI

app = FastAPI(title="Personal Finance Monitor")


@app.get("/")
def root():
    return {"message": "Personal Finance Monitor is alive!"}