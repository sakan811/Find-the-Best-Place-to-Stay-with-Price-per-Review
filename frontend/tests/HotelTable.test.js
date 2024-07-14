import React from 'react';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import axios from 'axios';
import HotelTable from "../src/components/HotelTable";


jest.mock('axios');
jest.mock('react-helmet-async', () => ({
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
    axios.get.mockImplementation((url) => {
      if (url.includes('get_hotel_data_from_db')) {
        return Promise.resolve({ data: { hotel_data: mockHotelData } });
      } else if (url.includes('get_booking_details_from_db')) {
        return Promise.resolve({ data: { booking_data: mockBookingDetails } });
      }
    });
    axios.post.mockResolvedValue({ data: { filename: 'test.xlsx', file_content: 'base64encodedcontent' } });

    // Mock window.URL.createObjectURL
    window.URL.createObjectURL = jest.fn();
    window.URL.revokeObjectURL = jest.fn();
  });

  test('renders HotelTable component', async () => {
    await act(async () => {
      render(<HotelTable />);
    });
    expect(screen.getByText('Hotels\' Room Price/Review Data')).toBeInTheDocument();
  });

  test('displays hotel data correctly', async () => {
    await act(async () => {
      render(<HotelTable />);
    });
    expect(screen.getByText('Hotel A')).toBeInTheDocument();
    expect(screen.getByText('Hotel B')).toBeInTheDocument();
  });

  test('displays booking details correctly', async () => {
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

  test('handles save data button click', async () => {
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

  test('handles error when saving data', async () => {
    axios.post.mockRejectedValueOnce(new Error('Network error'));

    await act(async () => {
      render(<HotelTable />);
    });
    const saveButton = screen.getByText('Save Data to Excel');

    await act(async () => {
      fireEvent.click(saveButton);
    });

    expect(screen.getByText('Error!')).toBeInTheDocument();
  });

  test('handles back to form button click', async () => {
    delete window.location;
    window.location = { href: jest.fn() };

    await act(async () => {
      render(<HotelTable />);
    });
    const backButton = screen.getByText('Back to Form');

    fireEvent.click(backButton);

    expect(window.location.href).toBe('/');
  });

  test('formats numbers correctly', async () => {
    await act(async () => {
      render(<HotelTable />);
    });
    expect(screen.getByText('200.00')).toBeInTheDocument();
    expect(screen.getByText('23.53')).toBeInTheDocument();
  });
});