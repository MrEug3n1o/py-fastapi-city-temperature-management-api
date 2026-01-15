import asyncio
import httpx


async def get_coordinates(city_name: str):
    url = "https://geocoding-api.open-meteo.com/v1/search" f"?name={city_name}&count=1"
    async with httpx.AsyncClient(timeout=9) as client:
        x = await client.get(url)
        return x.json()
async def get_weather(city_name: str):
    lat, lon = await get_coordinates(city_name)
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )
    async with httpx.AsyncClient(timeout=9) as client:
        x = await client.get(url)
        return x.json()
