import httpx
from fastapi import HTTPException

from app.schemas.route import RouteOption, RoutesResponse


async def fetch_routes(
    start_lat: float,
    start_lng: float,
    end_lat: float,
    end_lng: float
) -> RoutesResponse:

    coordinates = (
        f"{start_lng},{start_lat};"
        f"{end_lng},{end_lat}"
    )

    url = (
        "https://router.project-osrm.org"
        f"/route/v1/driving/{coordinates}"
    )

    params = {
        "alternatives": "true",
        "overview": "full",
        "geometries": "geojson"
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

    except (httpx.HTTPError, ValueError) as exc:
        raise HTTPException(
            status_code=502,
            detail="Routing service unavailable"
        ) from exc

    if data.get("code") != "Ok" or not data.get("routes"):
        raise HTTPException(
            status_code=404,
            detail="No route found"
        )

    routes = []

    for index, route in enumerate(data["routes"]):
        routes.append(
            RouteOption(
                id=index,
                distance=round(route["distance"] / 1000, 2),
                duration=round(route["duration"] / 60, 1),
                coordinates=[
                    (point[1], point[0])
                    for point in route["geometry"]["coordinates"]
                ]
            )
        )

    return RoutesResponse(routes=routes)