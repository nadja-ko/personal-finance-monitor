from datetime import date

from pydantic import BaseModel


class TripCreate(BaseModel):
    name: str
    start_date: date
    end_date: date | None = None


class TripResponse(TripCreate):
    id: int
