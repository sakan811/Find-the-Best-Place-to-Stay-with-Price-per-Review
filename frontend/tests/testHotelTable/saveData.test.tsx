import { render, screen, fireEvent } from '@testing-library/react';
import { vi, describe, beforeEach, it, expect } from 'vitest';

import axios from 'axios';
import HotelTable from "../../src/components/HotelTable";
import React from "react";

vi.mock('axios');

vi.mock('react-helmet-async', () => ({
  Helmet: () => <div></div>,
}));

// Mocking URL.createObjectURL and revokeObjectURL
(window.URL as unknown) = {
    createObjectURL: vi.fn(() => 'mocked-url'),
    revokeObjectURL: vi.fn(),
};


describe('HotelTable Component', () => {
    beforeEach(() => {
        // Clear all previous mocks
        vi.clearAllMocks();
    });

    it('should save data successfully and show success message', async () => {
        const mockHotelData = [
            {
                city: 'New York',
                hotel: 'Hotel A',
                review_score: 4.5,
                room_price: 200,
                price_per_review: 44.44,
                check_in: '2023-10-01',
                check_out: '2023-10-05',
            },
        ];

        const mockResponse = {
            filename: 'test.xlsx',
            file_content: btoa('mock file content'), // Base64 encode a string
        };

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

        (axios.get as jest.Mock)
          .mockResolvedValueOnce({ data: { hotel_data: mockHotelData } }) // Mock fetchData
          .mockResolvedValueOnce({ data: { booking_data: bookingDetails } }); // Mock fetchBookingDetails

        // Mocking the POST request to save data
        (axios.post as jest.Mock).mockResolvedValueOnce({ data: mockResponse });

        render(<HotelTable />);

        // Click the save data button
        fireEvent.click(screen.getByText(/Save Data to Excel/i));

        // Wait for the success message to appear
        const successMessage = await screen.findByText(/Saved data to Excel successfully/i);
        expect(successMessage).toBeInTheDocument();

        expect(URL.createObjectURL).toHaveBeenCalled();
    });

    it('should show error message when saving data fails', async () => {
        // Mocking the POST request to fail
        (axios.post as jest.Mock).mockRejectedValueOnce(new Error('Network Error'));

        render(<HotelTable />);

        // Click the save data button
        fireEvent.click(screen.getByText(/Save Data to Excel/i));

        // Wait for the error message to appear
        const errorMessage = await screen.findByText(/Failed to save data/i);
        expect(errorMessage).toBeInTheDocument();
    });
});
