import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { HelmetProvider } from 'react-helmet-async';
import App from '../src/App';

describe('App Component', () => {
  it('renders ScrapingForm route', () => {
    render(
      <HelmetProvider>
          <App />
      </HelmetProvider>
    );

    // Check text on the ScrapingForm route
    expect(screen.getByText(/Finding the Best Place to Stay with Price\/Review from Booking.com/i)).toBeInTheDocument();
    expect(screen.getByText(/Enter the hotel booking details below to scrape the hotel data/i)).toBeInTheDocument();
  });

  it('renders HotelTable route', () => {
    // Simulate navigation to /hotel_data_table_page
    window.history.pushState({}, '', '/hotel_data_table_page');

    render(
      <HelmetProvider>
          <App />
      </HelmetProvider>
    );

    // Check text on the HotelTable route
    expect(screen.getByText(/Hotels' Room Price\/Review Data/i)).toBeInTheDocument();
    expect(screen.getByText(/Save Data to Excel/i)).toBeInTheDocument();
    expect(screen.getByText(/Booking Details/i)).toBeInTheDocument();
  });
});
