from fastapi import FastAPI

from backend.api.accounts import router as accounts_router
from backend.database.connection import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Finance Monitor")

app.include_router(accounts_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Personal Finance Monitor is alive!"}
