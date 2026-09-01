from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.models.trips import TripDB
from backend.schemas.trips import TripCreate, TripResponse

router = APIRouter(prefix="/trips", tags=["trips"])


@router.post("/", response_model=TripResponse)
def create_trip(
    trip: TripCreate,
    db: Session = Depends(get_db),  # noqa: B008
) -> TripDB:
    """
    Create a new trip in the database.
    """
    db_trip = TripDB(
        name=trip.name,
        start_date=trip.start_date,
        end_date=trip.end_date,
    )

    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)

    return db_trip


@router.get("/", response_model=list[TripResponse])
def get_trips(
    db: Session = Depends(get_db),  # noqa: B008
) -> list[TripDB]:
    """
    Retrieve all trips from the database.
    """
    return db.query(TripDB).all()
