import { Component, Input, Output, EventEmitter } from '@angular/core';

import { Location } from '../../models/location.model';

@Component({
  selector: 'app-location-selector',
  standalone: false,
  templateUrl: './location-selector.component.html',
  styleUrl: './location-selector.component.css',
})
export class LocationSelectorComponent {
  
  @Input() departure: Location | null = null;
  @Input() destination: Location | null = null;

  @Output() reset = new EventEmitter<void>();

  resetSelection(): void {
    this.reset.emit();
  }
}
