import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, vi } from 'vitest';
import HotelTable from "../../src/components/HotelTable";
import React from "react";

vi.mock('react-helmet-async', () => ({
  Helmet: () => <div></div>,
}));

describe('HotelTable Component', () => {
    it('should redirect to the form page when the button is clicked', () => {
        // Mock window.location
        const originalLocation = window.location;
        const mockLocation = { href: '' };
        Object.defineProperty(window, 'location', {
            value: mockLocation,
            writable: true,
        });

        render(<HotelTable />);

        const button = screen.getByText('Back to Form');
        fireEvent.click(button);

        expect(mockLocation.href).toBe('/');

        // Restore original window.location
        Object.defineProperty(window, 'location', {
            value: originalLocation,
            writable: true,
        });
    });

    it('should log an error if redirection fails', () => {
        // Mock console.error
        const consoleErrorMock = vi.spyOn(console, 'error').mockImplementation(() => {});

        // Mock window.location to throw an error
        const originalLocation = window.location;
        const mockLocation = {
            set "href"(_: string) {
                throw new Error('Redirection error');
            },
        };
        Object.defineProperty(window, 'location', {
            value: mockLocation,
            writable: true,
        });

        render(<HotelTable />);

        const button = screen.getByText('Back to Form');
        fireEvent.click(button);

        expect(consoleErrorMock).toHaveBeenCalledWith('Error redirecting to form page:', expect.any(Error));

        // Restore original window.location and console.error
        Object.defineProperty(window, 'location', {
            value: originalLocation,
            writable: true,
        });
        consoleErrorMock.mockRestore();
    });
});