from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import httpx

from app.database import get_db
from app.models import City
from app.schemas import TemperatureList
import app.crud as crud

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.post("/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(City).all()

    async with httpx.AsyncClient() as client:
        for city in cities:
            url = (
                "https://api.open-meteo.com/v1/forecast"
                "?latitude=52.52&longitude=13.41&current_weather=true"
            )
            response = await client.get(url)
            response.raise_for_status()

            temperature = response.json()["current_weather"]["temperature"]
            crud.create_temperature(db, city.id, temperature)

    return {"detail": "Temperature data updated successfully"}


@router.get("/", response_model=list[TemperatureList])
def get_temperatures_endpoint(
    city_id: int | None = None,
    db: Session = Depends(get_db)
):
    return crud.get_temperatures(db, city_id)
