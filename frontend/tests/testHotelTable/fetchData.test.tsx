import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import axios from 'axios';
import HotelTable from "../../src/components/HotelTable";
import React from "react";

vi.mock('axios');
vi.mock('react-helmet-async', () => ({
  Helmet: () => <div></div>,
}));

const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('HotelTable Component', () => {
    it('should fetch and display hotel data', async () => {
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

        mockedAxios.get.mockResolvedValueOnce({
            data: { hotel_data: mockHotelData },
        });

        render(<HotelTable />);

        await waitFor(() => {
            expect(screen.getByText('New York')).toBeInTheDocument();
            expect(screen.getByText('Hotel A')).toBeInTheDocument();
            expect(screen.getByText('4.50')).toBeInTheDocument();
            expect(screen.getByText('200.00')).toBeInTheDocument();
            expect(screen.getByText('44.44')).toBeInTheDocument();
            expect(screen.getByText('2023-10-01')).toBeInTheDocument();
            expect(screen.getByText('2023-10-05')).toBeInTheDocument();
        });
    });

    it('should handle fetch error', async () => {
        mockedAxios.get.mockRejectedValueOnce(new Error('Error fetching data'));

        render(<HotelTable />);

        await waitFor(() => {
            expect(screen.queryByText('New York')).not.toBeInTheDocument();
        });
    });
});