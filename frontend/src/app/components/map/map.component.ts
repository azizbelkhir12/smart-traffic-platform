import {
  Component,
  AfterViewInit,
  OnDestroy,
  ElementRef,
  ViewChild,
  EventEmitter,
  Input,
  Output,
  OnChanges,
  SimpleChanges,
} from '@angular/core';
import { RouteOption } from '../../models/route.model';

import * as L from 'leaflet';
import { Location } from '../../models/location.model';

@Component({
  selector: 'app-map',
  standalone: false,
  templateUrl: './map.component.html',
  styleUrl: './map.component.css',
})
export class MapComponent implements AfterViewInit, OnDestroy {
  @ViewChild('mapContainer')
  mapContainer!: ElementRef<HTMLDivElement>;

  @Input() departure: Location | null = null;
  @Input() destination: Location | null = null;

  @Output() locationSelected = new EventEmitter<Location>();
  @Input() routes: RouteOption[] = [];

  private routeLayer?: L.LayerGroup;
  private map?: L.Map;
  private departureMarker?: L.CircleMarker;
  private destinationMarker?: L.CircleMarker;

  ngAfterViewInit(): void {
    this.map = L.map(this.mapContainer.nativeElement, {
      center: [36.8065, 10.1815],
      zoom: 14,
      zoomControl: true,
    });

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; OpenStreetMap contributors',
    }).addTo(this.map);

    this.map.on('click', (event: L.LeafletMouseEvent) => {
      this.locationSelected.emit({
        lat: event.latlng.lat,
        lng: event.latlng.lng,
      });
    });

    this.updateMarkers();
    this.drawRoutes();
  }

 ngOnChanges(changes: SimpleChanges): void {
  this.updateMarkers();

  if (changes['routes']) {
    this.drawRoutes();
  }
}

private drawRoutes(): void {
  if (!this.map) return;

  this.routeLayer?.remove();
  this.routeLayer = L.layerGroup().addTo(this.map);

  const bounds = L.latLngBounds([]);

  this.routes.forEach((route, index) => {
    const line = L.polyline(route.coordinates, {
      color: index === 0 ? '#2563eb' : '#64748b',
      weight: index === 0 ? 6 : 4,
      opacity: index === 0 ? 0.9 : 0.65
    }).addTo(this.routeLayer!);

    line.bindPopup(
      `Route ${index + 1}<br>` +
      `${route.distance} km<br>` +
      `${route.duration} min`
    );

    bounds.extend(line.getBounds());
  });

  if (bounds.isValid()) {
    this.map.fitBounds(bounds, {
      padding: [50, 50],
      maxZoom: 15
    });
  }
}

  private updateMarkers(): void {
    if (!this.map) return;

    this.departureMarker?.remove();
    this.destinationMarker?.remove();

    if (this.departure) {
      this.departureMarker = L.circleMarker(
        [this.departure.lat, this.departure.lng],
        {
          radius: 9,
          color: '#ffffff',
          weight: 2,
          fillColor: '#22c55e',
          fillOpacity: 1,
        },
      ).addTo(this.map);

      this.departureMarker.bindPopup('Departure');
    }

    if (this.destination) {
      this.destinationMarker = L.circleMarker(
        [this.destination.lat, this.destination.lng],
        {
          radius: 9,
          color: '#ffffff',
          weight: 2,
          fillColor: '#ef4444',
          fillOpacity: 1,
        },
      ).addTo(this.map);

      this.destinationMarker.bindPopup('Destination');
    }
  }

  ngOnDestroy(): void {
    this.map?.remove();
  }
}
