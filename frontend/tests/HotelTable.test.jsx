import React from 'react';
import { render, screen, fireEvent, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import axios from 'axios';
import HotelTable from "../src/components/HotelTable";
import { describe, it, beforeEach, expect, vi } from 'vitest';

vi.mock('axios');
vi.mock('react-helmet-async', () => ({
  Helmet: ({ children }) => <div data-testid="helmet-mock">{children}</div>,
}));

const mockHotelData = [
  { city: 'New York', hotel: 'Hotel A', review_score: 8.5, room_price: 200, price_per_review: 23.53, check_in: '2023-07-01', check_out: '2023-07-05' },
  { city: 'Paris', hotel: 'Hotel B', review_score: 9.0, room_price: 250, price_per_review: 27.78, check_in: '2023-07-02', check_out: '2023-07-06' },
];

const mockBookingDetails = [
  { city: 'New York', check_in: '2023-07-01', check_out: '2023-07-05', num_adults: 2, num_children: 1, num_rooms: 1, currency: 'USD', only_hotel: true },
];

describe('HotelTable Component', () => {
  beforeEach(() => {
    vi.mocked(axios.get).mockImplementation((url) => {
      if (url.includes('get_hotel_data_from_db')) {
        return Promise.resolve({ data: { hotel_data: mockHotelData } });
      } else if (url.includes('get_booking_details_from_db')) {
        return Promise.resolve({ data: { booking_data: mockBookingDetails } });
      }
    });
    vi.mocked(axios.post).mockResolvedValue({ data: { filename: 'test.xlsx', file_content: 'base64encodedcontent' } });

    // Mock window.URL.createObjectURL
    window.URL.createObjectURL = vi.fn();
    window.URL.revokeObjectURL = vi.fn();
  });

  it('renders HotelTable component', async () => {
    await act(async () => {
      render(<HotelTable />);
    });
    expect(screen.getByText('Hotels\' Room Price/Review Data')).toBeInTheDocument();
  });

  it('displays hotel data correctly', async () => {
    await act(async () => {
      render(<HotelTable />);
    });
    expect(screen.getByText('Hotel A')).toBeInTheDocument();
    expect(screen.getByText('Hotel B')).toBeInTheDocument();
  });

  it('displays booking details correctly', async () => {
    await act(async () => {
      render(<HotelTable />);
    });
    expect(screen.getByText('City', { selector: 'strong' })).toBeInTheDocument();
    expect(screen.getByText(': New York')).toBeInTheDocument();
    expect(screen.getByText('Check In', { selector: 'strong' })).toBeInTheDocument();
    expect(screen.getByText(': 2023-07-01')).toBeInTheDocument();
    expect(screen.getByText('Check Out', { selector: 'strong' })).toBeInTheDocument();
    expect(screen.getByText(': 2023-07-05')).toBeInTheDocument();
    expect(screen.getByText('Adults', { selector: 'strong' })).toBeInTheDocument();
    expect(screen.getByText(': 2')).toBeInTheDocument();
    expect(screen.getByText('Children', { selector: 'strong' })).toBeInTheDocument();
    expect(screen.getAllByText(': 1')[0]).toBeInTheDocument();
    expect(screen.getByText('Rooms', { selector: 'strong' })).toBeInTheDocument();
    expect(screen.getAllByText(': 1')[1]).toBeInTheDocument();
    expect(screen.getByText('Currency', { selector: 'strong' })).toBeInTheDocument();
    expect(screen.getByText(': USD')).toBeInTheDocument();
  });

  it('handles save data button click', async () => {
    await act(async () => {
      render(<HotelTable />);
    });
    const saveButton = screen.getByText('Save Data to Excel');

    await act(async () => {
      fireEvent.click(saveButton);
    });

    expect(axios.post).toHaveBeenCalledWith('http://localhost:8000/save/', {}, { responseType: 'json' });
    expect(screen.getByText('Success!')).toBeInTheDocument();

    expect(window.URL.createObjectURL).toHaveBeenCalled();
    expect(window.URL.revokeObjectURL).toHaveBeenCalled();
  });

  it('handles error when saving data', async () => {
    vi.mocked(axios.post).mockRejectedValueOnce(new Error('Network error'));

    await act(async () => {
      render(<HotelTable />);
    });
    const saveButton = screen.getByText('Save Data to Excel');

    await act(async () => {
      fireEvent.click(saveButton);
    });

    expect(screen.getByText('Error!')).toBeInTheDocument();
  });

  it('handles back to form button click', async () => {
    delete window.location;
    window.location = { href: vi.fn() };

    await act(async () => {
      render(<HotelTable />);
    });
    const backButton = screen.getByText('Back to Form');

    fireEvent.click(backButton);

    expect(window.location.href).toBe('/');
  });

  it('formats numbers correctly', async () => {
    await act(async () => {
      render(<HotelTable />);
    });
    expect(screen.getByText('200.00')).toBeInTheDocument();
    expect(screen.getByText('23.53')).toBeInTheDocument();
  });
});
