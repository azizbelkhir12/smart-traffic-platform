import {
  Component,
  AfterViewInit,
  OnDestroy,
  ElementRef,
  ViewChild,
  EventEmitter,
  Input,
  Output
} from '@angular/core';

import * as L from 'leaflet';
import { Location } from '../../models/location.model';

@Component({
  selector: 'app-map',
  standalone: false,
  templateUrl: './map.component.html',
  styleUrl: './map.component.css'
})
export class MapComponent implements AfterViewInit, OnDestroy {

 @ViewChild('mapContainer')
  mapContainer!: ElementRef<HTMLDivElement>;

 @Input() departure: Location | null = null;
@Input() destination: Location | null = null;

@Output() locationSelected = new EventEmitter<Location>();

  private map?: L.Map;
  private departureMarker?: L.CircleMarker;
  private destinationMarker?: L.CircleMarker;

  ngAfterViewInit(): void {
    this.map = L.map(this.mapContainer.nativeElement, {
      center: [36.8065, 10.1815],
      zoom: 12,
      zoomControl: true
    });

    L.tileLayer(
      'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
      {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors'
      }
    ).addTo(this.map);

    this.map.on('click', (event: L.LeafletMouseEvent) => {
      this.locationSelected.emit({
        lat: event.latlng.lat,
        lng: event.latlng.lng
      });
    });

    this.updateMarkers();
  }

  ngOnChanges(): void {
    this.updateMarkers();
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
          fillOpacity: 1
        }
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
          fillOpacity: 1
        }
      ).addTo(this.map);

      this.destinationMarker.bindPopup('Destination');
    }
  }

  ngOnDestroy(): void {
    this.map?.remove();
  }

}
