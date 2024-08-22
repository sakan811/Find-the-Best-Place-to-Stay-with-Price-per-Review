import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import axios from 'axios';

import { HelmetProvider } from 'react-helmet-async';
import ScrapingForm from "../src/components/ScrapingForm";

// Mock axios
vi.mock('axios');

// Mock react-helmet-async
vi.mock('react-helmet-async', () => ({
  Helmet: ({ children }) => <div data-testid="helmet-mock">{children}</div>,
  HelmetProvider: ({ children }) => <div data-testid="helmet-provider-mock">{children}</div>,
}));

describe('ScrapingForm Component', () => {
  beforeEach(() => {
    render(
      <HelmetProvider>
        <ScrapingForm />
      </HelmetProvider>
    );
  });

  it('should submit the form and handle a successful submission', async () => {
    // Mock a successful axios post response
    axios.post.mockResolvedValue({ data: { message: 'Success' } });

    // Simulate user input
    fireEvent.change(screen.getByLabelText(/City:/i), { target: { value: 'Osaka' } });
    fireEvent.change(screen.getByLabelText(/Country:/i), { target: { value: 'Japan' } });
    fireEvent.change(screen.getByLabelText(/Check-in:/i), { target: { value: '2024-09-01' } });
    fireEvent.change(screen.getByLabelText(/Check-out:/i), { target: { value: '2024-09-05' } });
    fireEvent.change(screen.getByLabelText(/Adults:/i), { target: { value: 2 } });
    fireEvent.change(screen.getByLabelText(/Rooms:/i), { target: { value: 1 } });
    fireEvent.change(screen.getByLabelText(/Children:/i), { target: { value: 0 } });
    fireEvent.change(screen.getByLabelText(/Currency:/i), { target: { value: 'USD' } });
    fireEvent.click(screen.getByLabelText(/Scrape Hotel Properties Only:/i));

    // Simulate form submission
    fireEvent.submit(screen.getByRole('button', { name: /Submit/i }));

    // Wait for form submission to complete
    await screen.findByText(/Form submitted successfully/i);

    // Check if the success message appears
    expect(screen.getByText(/Form submitted successfully/i)).toBeInTheDocument();
  });

  it('should handle a failed submission', async () => {
    // Mock a failed axios post response
    axios.post.mockRejectedValue({ response: { status: 500, data: { error: 'Internal Server Error' } } });

    // Simulate user input
    fireEvent.change(screen.getByLabelText(/City:/i), { target: { value: 'Tokyo' } });
    fireEvent.change(screen.getByLabelText(/Country:/i), { target: { value: 'Japan' } });
    fireEvent.change(screen.getByLabelText(/Check-in:/i), { target: { value: '2024-09-01' } });
    fireEvent.change(screen.getByLabelText(/Check-out:/i), { target: { value: '2024-09-05' } });
    fireEvent.change(screen.getByLabelText(/Adults:/i), { target: { value: 2 } });
    fireEvent.change(screen.getByLabelText(/Rooms:/i), { target: { value: 1 } });
    fireEvent.change(screen.getByLabelText(/Children:/i), { target: { value: 0 } });
    fireEvent.change(screen.getByLabelText(/Currency:/i), { target: { value: 'USD' } });
    fireEvent.click(screen.getByLabelText(/Scrape Hotel Properties Only:/i));

    // Simulate form submission
    fireEvent.submit(screen.getByRole('button', { name: /Submit/i }));

    // Wait for error message to appear
    await screen.findByText(/Internal server error/i);

    // Check if the error message appears
    expect(screen.getByText(/Internal server error/i)).toBeInTheDocument();
  });

  it('should handle a system exit error', async () => {
    // Mock a failed axios post response
    axios.post.mockRejectedValue({ response: { status: 500, data: { error: 'SystemExit' } } });

    // Simulate user input
    fireEvent.change(screen.getByLabelText(/City:/i), { target: { value: 'Tokyo' } });
    fireEvent.change(screen.getByLabelText(/Country:/i), { target: { value: 'Japan' } });
    fireEvent.change(screen.getByLabelText(/Check-in:/i), { target: { value: '2024-09-01' } });
    fireEvent.change(screen.getByLabelText(/Check-out:/i), { target: { value: '2024-09-05' } });
    fireEvent.change(screen.getByLabelText(/Adults:/i), { target: { value: 2 } });
    fireEvent.change(screen.getByLabelText(/Rooms:/i), { target: { value: 1 } });
    fireEvent.change(screen.getByLabelText(/Children:/i), { target: { value: 0 } });
    fireEvent.change(screen.getByLabelText(/Currency:/i), { target: { value: 'USD' } });
    fireEvent.click(screen.getByLabelText(/Scrape Hotel Properties Only:/i));

    // Simulate form submission
    fireEvent.submit(screen.getByRole('button', { name: /Submit/i }));

    // Wait for error message to appear
    await screen.findByText(/No places found that can satisfy this booking. Please re-enter the form./i);

    // Check if the error message appears
    expect(screen.getByText(/No places found that can satisfy this booking. Please re-enter the form./i)).toBeInTheDocument();
  });
});