import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import ScrapingForm from "../src/components/ScrapingForm";
import {HelmetProvider} from "react-helmet-async";

// Mock react-helmet-async
vi.mock('react-helmet-async', () => ({
  Helmet: ({ children }) => <div data-testid="helmet-mock">{children}</div>,
  HelmetProvider: ({ children }) => <div data-testid="helmet-provider-mock">{children}</div>,
}));

describe('ScrapingForm', () => {
    test('updates formData on input change', () => {
        const { getByLabelText } = render(
                                                                                  <HelmetProvider>
                                                                                    <ScrapingForm />
                                                                                  </HelmetProvider>
                                                                                );

        // Get input elements
        const cityInput = getByLabelText(/city/i);
        const checkInInput = getByLabelText(/check-in/i);
        const checkOutInput = getByLabelText(/check-out/i);
        const adultsInput = getByLabelText(/adults/i);
        const roomsInput = getByLabelText(/rooms/i);
        const childrenInput = getByLabelText(/children/i);
        const currencyInput = getByLabelText(/currency/i);
        const hotelFilterInput = getByLabelText(/scrape hotel properties only/i);

        // Simulate user input
        fireEvent.change(cityInput, { target: { name: 'city', value: 'New York' } });
        fireEvent.change(checkInInput, { target: { name: 'check_in', value: '2023-08-01' } });
        fireEvent.change(checkOutInput, { target: { name: 'check_out', value: '2023-08-10' } });
        fireEvent.change(adultsInput, { target: { name: 'group_adults', value: 2 } });
        fireEvent.change(roomsInput, { target: { name: 'num_rooms', value: 2 } });
        fireEvent.change(childrenInput, { target: { name: 'group_children', value: 1 } });
        fireEvent.change(currencyInput, { target: { name: 'selected_currency', value: 'USD' } });
        fireEvent.click(hotelFilterInput);

        // Assert state updates
        expect(cityInput.value).toBe('New York');
        expect(checkInInput.value).toBe('2023-08-01');
        expect(checkOutInput.value).toBe('2023-08-10');
        expect(adultsInput.value).toBe('2');
        expect(roomsInput.value).toBe('2');
        expect(childrenInput.value).toBe('1');
        expect(currencyInput.value).toBe('USD');
        expect(hotelFilterInput.checked).toBe(true);
    });
});
