from fastapi import FastAPI

from backend.api.accounts import router as accounts_router
from backend.api.categories import router as categories_router
from backend.api.transactions import router as transactions_router
from backend.database.connection import Base, engine
from backend.models.account import AccountDB  # noqa: F401
from backend.models.category import CategoryDB  # noqa: F401
from backend.models.transaction import TransactionDB  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Finance Monitor")

app.include_router(accounts_router)
app.include_router(transactions_router)
app.include_router(categories_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Personal Finance Monitor is alive!"}
