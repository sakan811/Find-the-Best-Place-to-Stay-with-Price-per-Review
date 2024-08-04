import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import axios from 'axios';

import { HelmetProvider } from 'react-helmet-async';
import ScrapingForm from "../src/components/ScrapingForm";

// Mock axios
jest.mock('axios');

// Mock react-helmet-async
jest.mock('react-helmet-async', () => ({
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

  test('handles no places found error', async () => {
    axios.post.mockRejectedValue({
      response: {
        status: 400,
        data: { error: 'SystemExit' }
      }
    });

    // Fill out the form
    fireEvent.change(screen.getByLabelText('City:'), { target: { value: 'New York' } });
    fireEvent.change(screen.getByLabelText('Check-in:'), { target: { value: '2023-07-01' } });
    fireEvent.change(screen.getByLabelText('Check-out:'), { target: { value: '2023-07-05' } });
    fireEvent.change(screen.getByLabelText('Currency:'), { target: { value: 'USD' } });

    fireEvent.click(screen.getByRole('button', { name: 'Submit' }));

    await waitFor(() => {
      expect(screen.getByText('No places found that can satisfy this booking. Please re-enter the form.')).toBeInTheDocument();
    });
  });

  test('displays any error message after form submission failure', async () => {
    axios.post.mockRejectedValue({
      response: {
        status: 400,
        data: {}
      }
    });

    // Fill out the form
    fireEvent.change(screen.getByLabelText('City:'), { target: { value: 'New York' } });
    fireEvent.change(screen.getByLabelText('Check-in:'), { target: { value: '2023-07-01' } });
    fireEvent.change(screen.getByLabelText('Check-out:'), { target: { value: '2023-07-05' } });
    fireEvent.change(screen.getByLabelText('Currency:'), { target: { value: 'USD' } });

    fireEvent.click(screen.getByRole('button', { name: 'Submit' }));

    await waitFor(() => {
      const errorElement = screen.getByText((content, element) => {
        return element.classList.contains('errorMessage');
      });
      expect(errorElement).toBeInTheDocument();
    });
  });
});