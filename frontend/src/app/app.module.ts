import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { provideHttpClient } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { MapComponent } from './components/map/map.component';
import { LocationSelectorComponent } from './components/location-selector/location-selector.component';
import { RouteListComponent } from './components/route-list/route-list.component';

@NgModule({
  declarations: [
    AppComponent,
    MapComponent,
    LocationSelectorComponent,
    RouteListComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [provideHttpClient()],
  bootstrap: [AppComponent]
})
export class AppModule { }
