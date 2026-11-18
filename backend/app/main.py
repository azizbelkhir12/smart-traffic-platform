
import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Smart Traffic Platform API",
    description="Backend API for Smart Traffic Platform",
    version="1.0.0"
)

# Allow Angular to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["GET"],
    allow_headers=["*"]
)


# Check backend status
@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "message": "Smart Traffic API is running"
    }


# Search for road routes
@app.get("/api/routes")
async def get_routes(
    start_lat: float = Query(ge=-90, le=90),
    start_lng: float = Query(ge=-180, le=180),
    end_lat: float = Query(ge=-90, le=90),
    end_lng: float = Query(ge=-180, le=180)
):
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
            detail="No route found between these locations"
        )

    routes = []

    for index, route in enumerate(data["routes"]):
        routes.append({
            "id": index,
            "distance": round(route["distance"] / 1000, 2),
            "duration": round(route["duration"] / 60, 1),
            "coordinates": [
                [point[1], point[0]]
                for point in route["geometry"]["coordinates"]
            ]
        })

    return {"routes": routes}
