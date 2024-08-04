import axios from "axios";
import {fireEvent, render, screen} from "@testing-library/react";
import {HelmetProvider} from "react-helmet-async";
import ScrapingForm from "../src/components/ScrapingForm";
import React from "react";
import '@testing-library/jest-dom';


// Mock axios
jest.mock('axios');

// Mock react-helmet-async
jest.mock('react-helmet-async', () => ({
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
    axios.post.mockRejectedValue({
      response: {
        status: 500,
        data: {}
      }
    });

    // Fill out the form
    fireEvent.change(screen.getByLabelText('City:'), { target: { value: 'New York' } });
    fireEvent.change(screen.getByLabelText('Check-in:'), { target: { value: '2023-07-01' } });
    fireEvent.change(screen.getByLabelText('Check-out:'), { target: { value: '2023-07-05' } });
    fireEvent.change(screen.getByLabelText('Currency:'), { target: { value: 'USD' } });

    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: 'Submit' }));

    const errorMessage = await screen.findByText('Internal server error. Please try again later.');

    // Ensure the error message is in the document
    expect(errorMessage).toBeInTheDocument();
  });
});
