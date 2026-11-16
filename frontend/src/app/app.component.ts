import { Component } from '@angular/core';
import { MapComponent } from './components/map/map.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: false,
  styleUrl: './app.component.css'
})
export class AppComponent {
 departure: Location | null = null;
  destination: Location | null = null;

  onLocationSelected(location: Location): void {
    if (!this.departure || this.destination) {
      this.departure = location;
      this.destination = null;
    } else {
      this.destination = location;
    }
  }

  resetLocations(): void {
    this.departure = null;
    this.destination = null;
  }
}
