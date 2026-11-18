from fastapi import APIRouter, Query

from app.schemas.route import RoutesResponse
from app.services.routing_service import fetch_routes

router = APIRouter(
    prefix="/api/routes",
    tags=["Routes"]
)


@router.get("", response_model=RoutesResponse)
async def get_routes(
    start_lat: float = Query(ge=-90, le=90),
    start_lng: float = Query(ge=-180, le=180),
    end_lat: float = Query(ge=-90, le=90),
    end_lng: float = Query(ge=-180, le=180)
):
    return await fetch_routes(
        start_lat=start_lat,
        start_lng=start_lng,
        end_lat=end_lat,
        end_lng=end_lng
    )