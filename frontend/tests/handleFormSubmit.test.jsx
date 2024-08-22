import axios from "axios";
import {fireEvent, render, screen} from "@testing-library/react";
import {HelmetProvider} from "react-helmet-async";
import ScrapingForm from "../src/components/ScrapingForm";
import React from "react";
import '@testing-library/jest-dom';


// Mock axios
vi.mock('axios');

// Mock react-helmet-async
vi.mock('react-helmet-async', () => ({
  Helmet: ({ children }) => <div data-testid="helmet-mock">{children}</div>,
  HelmetProvider: ({ children }) => <div data-testid="helmet-provider-mock">{children}</div>,
}));

describe('ScrapingForm Component', () => {
  render(
    <HelmetProvider>
      <ScrapingForm />
    </HelmetProvider>
  );

  test('handles form submission error', async () => {
    // Mock the axios POST request to simulate a server error
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

    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: 'Submit' }));

    // Wait for error message to appear
    await screen.findByText(/Internal server error/i);

    // Check if the error message appears
    expect(screen.getByText(/Internal server error/i)).toBeInTheDocument();
  });
});
