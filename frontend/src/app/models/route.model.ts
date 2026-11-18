export interface RouteOption {
  id: number;
  distance: number;
  duration: number;
  coordinates: [number, number][];
}

export interface RoutesResponse {
  routes: RouteOption[];
}