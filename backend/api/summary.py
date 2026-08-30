from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.schemas.summary import CashFlowSummary
from backend.services.summary import get_cash_flow_summary

router = APIRouter(prefix="/summary", tags=["summary"])


@router.get("/cash-flow", response_model=CashFlowSummary)
def cash_flow_summary(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),  # noqa: B008
) -> CashFlowSummary:
    """
    Retrieve the cash flow summary for a given date range.

    Args:
        start_date (date): The start date for the summary.
        end_date (date): The end date for the summary.
        db (Session): The database session.

    Returns:
        CashFlowSummary: The calculated cash flow summary.
    """
    return get_cash_flow_summary(
        db=db,
        start_date=start_date,
        end_date=end_date,
    )
