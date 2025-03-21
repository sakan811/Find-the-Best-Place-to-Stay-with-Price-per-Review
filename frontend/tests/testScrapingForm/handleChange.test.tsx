import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ScrapingForm from "../../src/components/ScrapingForm";
import { describe, vi, test, expect } from 'vitest';

describe('ScrapingForm', () => {
    test('updates formData on input change', () => {
        render(<ScrapingForm />);

        // Get input elements
        const cityInput = screen.getByRole('textbox', { name: /City:/i }) as HTMLInputElement;
        const checkInInput = screen.getByLabelText(/Check-in:/i) as HTMLInputElement;
        const checkOutInput = screen.getByLabelText(/Check-out:/i) as HTMLInputElement;
        const adultsInput = screen.getByRole('spinbutton', { name: /Adults:/i }) as HTMLInputElement;
        const roomsInput = screen.getByRole('spinbutton', { name: /Rooms:/i }) as HTMLInputElement;
        const childrenInput = screen.getByRole('spinbutton', { name: /Children:/i }) as HTMLInputElement;
        const currencyInput = screen.getByRole('textbox', { name: /Currency:/i }) as HTMLInputElement;
        const hotelFilterInput = screen.getByRole('checkbox', { name: /Scrape Hotel Properties Only:/i }) as HTMLInputElement;

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
