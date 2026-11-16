import { NO_ERRORS_SCHEMA } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { AppComponent } from './app.component';

describe('AppComponent', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AppComponent],
      schemas: [NO_ERRORS_SCHEMA],
    }).compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  it('should set the departure on the first selection', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    const location = { lat: 36.8065, lng: 10.1815 };

    app.onLocationSelected(location);

    expect(app.departure).toEqual(location);
    expect(app.destination).toBeNull();
  });

  it('should set the destination on the second selection', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    const departure = { lat: 36.8065, lng: 10.1815 };
    const destination = { lat: 36.8025, lng: 10.1885 };

    app.onLocationSelected(departure);
    app.onLocationSelected(destination);

    expect(app.departure).toEqual(departure);
    expect(app.destination).toEqual(destination);
  });

  it('should reset both selections', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    app.onLocationSelected({ lat: 36.8065, lng: 10.1815 });
    app.onLocationSelected({ lat: 36.8025, lng: 10.1885 });
    app.resetLocations();

    expect(app.departure).toBeNull();
    expect(app.destination).toBeNull();
  });
});
