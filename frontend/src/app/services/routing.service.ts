import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { Location } from '../models/location.model';
import { RoutesResponse } from '../models/route.model';

@Injectable({
  providedIn: 'root'
})
export class RoutingService {

  private readonly apiUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) { }

   getRoutes(
    departure: Location,
    destination: Location
  ): Observable<RoutesResponse> {

    const params = new HttpParams()
      .set('start_lat', departure.lat)
      .set('start_lng', departure.lng)
      .set('end_lat', destination.lat)
      .set('end_lng', destination.lng);

    return this.http.get<RoutesResponse>(
      `${this.apiUrl}/routes`,
      { params }
    );
  }
}
