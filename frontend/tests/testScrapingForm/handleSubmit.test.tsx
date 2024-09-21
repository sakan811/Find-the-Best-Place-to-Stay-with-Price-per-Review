import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, vi } from 'vitest';
import axios, {AxiosError} from 'axios';
import ScrapingForm from "../../src/components/ScrapingForm";
import React from "react";
import { expect } from 'vitest'

vi.mock('axios');
vi.mock('react-helmet-async', () => ({
  Helmet: () => <div></div>,
}));

describe('ScrapingForm handleSubmit', () => {
  const fillForm = () => {
    fireEvent.change(screen.getByLabelText(/City:/i), { target: { value: 'New York' } });
    fireEvent.change(screen.getByLabelText(/Country:/i), { target: { value: 'USA' } });
    fireEvent.change(screen.getByLabelText(/Check-in:/i), { target: { value: '2023-10-01' } });
    fireEvent.change(screen.getByLabelText(/Check-out:/i), { target: { value: '2023-10-10' } });
    fireEvent.change(screen.getByLabelText(/Adults:/i), { target: { value: 2 } });
    fireEvent.change(screen.getByLabelText(/Rooms:/i), { target: { value: 1 } });
    fireEvent.change(screen.getByLabelText(/Children:/i), { target: { value: 0 } });
    fireEvent.change(screen.getByLabelText(/Currency:/i), { target: { value: 'USD' } });
    fireEvent.click(screen.getByLabelText(/Scrape Hotel Properties Only:/i));
  };

  it('should display success message on successful form submission', async () => {
    (axios.post as jest.Mock).mockResolvedValue({ data: {} });

    render(<ScrapingForm />);
    fillForm();
    fireEvent.submit(screen.getByRole('button', { name: /Submit/i }));

    await waitFor(() => {
      expect(screen.getByText(/Form submitted successfully/i)).toBeInTheDocument();
    });
  });

  it('should display error message on form submission failure with SystemExit error', async () => {
    const mockError = {
      response: {
        data: { error: 'SystemExit' },
        status: 400
      },
      isAxiosError: true
    } as AxiosError;

    (axios.post as jest.Mock).mockRejectedValue(mockError);

    render(<ScrapingForm />);
    fillForm();
    fireEvent.submit(screen.getByRole('button', { name: /Submit/i }));

    await waitFor(() => {
      expect(screen.getByText(/No places found that can satisfy this booking. Please re-enter the form./i)).toBeInTheDocument();
    });
  });


  it('should display error message on form submission failure with 500 Internal Server Error', async () => {
    const mockError = {
      response: {
        data: { error: 'Internal Server Error' },
        status: 500
      },
      isAxiosError: true
    } as AxiosError;

    (axios.post as jest.Mock).mockRejectedValueOnce(mockError);

    render(<ScrapingForm />);
    fillForm();
    fireEvent.submit(screen.getByRole('button', { name: /Submit/i }));

    await waitFor(() => {
      expect(screen.getByText(/Internal server error. Please try again later./i)).toBeInTheDocument();
    });
  });


  it('should display generic error message on form submission failure with other errors', async () => {
    const mockError = {
      response: {
        data: {},
        status: 400
      },
      isAxiosError: true
    } as AxiosError;

    (axios.post as jest.Mock).mockRejectedValueOnce(mockError);

    render(<ScrapingForm />);
    fillForm();
    fireEvent.submit(screen.getByRole('button', { name: /Submit/i }));

    await waitFor(() => {
      expect(screen.getByText(/An error occurred while submitting the form./i)).toBeInTheDocument();
    });
  });
});