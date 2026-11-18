from pydantic import BaseModel


class RouteOption(BaseModel):
    id: int
    distance: float
    duration: float
    coordinates: list[tuple[float, float]]


class RoutesResponse(BaseModel):
    routes: list[RouteOption]