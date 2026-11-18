import { Component } from '@angular/core';
import { Subscription } from 'rxjs';
import { OnDestroy } from '@angular/core';

import { Location } from './models/location.model';
import { RouteOption } from './models/route.model';
import { RoutingService } from './services/routing.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: false,
  styleUrl: './app.component.css'
})
export class AppComponent {
  departure: Location | null = null;
  destination: Location | null = null;

 routes: RouteOption[] = [];
  loading = false;
  error = '';

  private request?: Subscription;

  constructor(private routingService: RoutingService) {}

  onLocationSelected(location: Location): void {
    if (!this.departure || this.destination) {
      this.cancelRequest();
      this.departure = location;
      this.destination = null;
      this.routes = [];
      this.error = '';
      return;
    }

    this.destination = location;
    this.loadRoutes();
  }

  loadRoutes(): void {
    if (!this.departure || !this.destination) return;

    this.cancelRequest();
    this.loading = true;
    this.error = '';
    this.routes = [];

    this.request = this.routingService
      .getRoutes(this.departure, this.destination)
      .subscribe({
        next: (response) => {
          this.routes = response.routes;
          this.loading = false;
        },
        error: () => {
          this.error = 'Unable to calculate routes.';
          this.loading = false;
        }
      });
  }

  resetLocations(): void {
    this.cancelRequest();
    this.departure = null;
    this.destination = null;
    this.routes = [];
    this.error = '';
  }

  private cancelRequest(): void {
    this.request?.unsubscribe();
    this.request = undefined;
    this.loading = false;
  }

  ngOnDestroy(): void {
    this.cancelRequest();
  }
}
