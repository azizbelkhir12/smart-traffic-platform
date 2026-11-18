import { Component, Input } from '@angular/core';
import { RouteOption } from '../../models/route.model';

@Component({
  selector: 'app-route-list',
  standalone: false,
  templateUrl: './route-list.component.html',
  styleUrl: './route-list.component.css'
})
export class RouteListComponent {
  @Input() routes: RouteOption[] = [];
}
