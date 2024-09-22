import { describe, it, expect, vi } from 'vitest';
import {render, screen, waitFor} from '@testing-library/react';
import React from "react";
import HotelTable from "../../src/components/HotelTable";
import axios from "axios";

vi.mock('react-helmet-async', () => ({
  Helmet: () => <div></div>,
}));

vi.mock('axios');

const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('HotelTable', () => {
    it('should format numbers correctly in the table', async () => {
        const mockData = [
            {
                city: 'New York',
                hotel: 'Hotel A',
                review_score: 4.567,
                room_price: 1234.567,
                price_per_review: 270.123,
                check_in: '2023-10-01',
                check_out: '2023-10-05',
            },
        ];

        // Mock the fetchData function to return mockData
        mockedAxios.get.mockResolvedValueOnce({
            data: {hotel_data: mockData},
        });


        render(<HotelTable/>);

        // Check if the formatted numbers are displayed correctly
        await waitFor(() => {
            expect(screen.getByText('4.57')).toBeInTheDocument();
            expect(screen.getByText('1,234.57')).toBeInTheDocument();
            expect(screen.getByText('270.12')).toBeInTheDocument();
        });
    });
});