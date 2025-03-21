import { describe, it, expect, vi, beforeAll, afterEach } from 'vitest';
import axios from 'axios';
import { render, screen, waitFor } from '@testing-library/react';
import HotelTable from '../../src/components/HotelTable';
import React from 'react';

vi.mock('axios');

const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('HotelTable Component', () => {
  beforeAll(() => {
    vi.spyOn(axios, 'get');
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('should fetch and display hotel data and booking details', async () => {
    const hotelData = [
      {
        city: 'New York',
        hotel: 'Hotel ABC',
        review_score: 8.5,
        room_price: 150,
        price_per_review: 17.65,
        check_in: '2023-10-01',
        check_out: '2023-10-05',
        accommodation_name: 'Hotels'
      },
    ];

    const bookingDetails = [
      {
        city: 'New York',
        check_in: '2023-10-01',
        check_out: '2023-10-05',
        num_adults: 2,
        num_children: 1,
        num_rooms: 1,
        currency: 'USD',
        only_hotel: true,
      },
    ];

    mockedAxios.get
      .mockResolvedValueOnce({ data: { hotel_data: hotelData } }) // Mock fetchData
      .mockResolvedValueOnce({ data: { booking_data: bookingDetails } }); // Mock fetchBookingDetails

    render(<HotelTable />);

    await waitFor(() => {
      // Check hotel data
      expect(screen.getByText('Hotel ABC')).toBeInTheDocument();
      expect(screen.getByText('8.50')).toBeInTheDocument();
      expect(screen.getByText('150.00')).toBeInTheDocument();
      expect(screen.getByText('17.65')).toBeInTheDocument();

      // Check booking details
      expect(screen.getByText('City', { selector: 'strong' })).toBeInTheDocument();
      expect(screen.getByText(': New York')).toBeInTheDocument();
      expect(screen.getByText('Check In', { selector: 'strong' })).toBeInTheDocument();
      expect(screen.getByText(': 2023-10-01')).toBeInTheDocument();
      expect(screen.getByText('Check Out', { selector: 'strong' })).toBeInTheDocument();
      expect(screen.getByText(': 2023-10-05')).toBeInTheDocument();
      expect(screen.getByText('Adults', { selector: 'strong' })).toBeInTheDocument();
      expect(screen.getByText(': 2')).toBeInTheDocument();
      expect(screen.getByText('Children', { selector: 'strong' })).toBeInTheDocument();
      expect(screen.queryAllByText(': 1')[1]).toBeInTheDocument();
      expect(screen.getByText('Rooms', { selector: 'strong' })).toBeInTheDocument();
      expect(screen.queryAllByText(': 1')[0]).toBeInTheDocument();
      expect(screen.getByText('Currency', { selector: 'strong' })).toBeInTheDocument();
      expect(screen.getByText(': USD')).toBeInTheDocument();
      expect(screen.getByText('Only Hotel Properties', { selector: 'strong' })).toBeInTheDocument();
      expect(screen.getByText(': true')).toBeInTheDocument();
      expect(screen.getByText('Hotels')).toBeInTheDocument();
    });
  });

  it('should handle fetch error', async () => {
    mockedAxios.get.mockRejectedValueOnce(new Error('Network Error'));

    render(<HotelTable />);

    await waitFor(() => {
      expect(screen.queryByText('New York')).not.toBeInTheDocument();
    });
  });
});