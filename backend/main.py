from fastapi import FastAPI

from backend.database.connection import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Finance Monitor")


@app.get("/")
def root():
    return {"message": "Personal Finance Monitor is alive!"}