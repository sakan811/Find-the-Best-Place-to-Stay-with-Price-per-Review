// __tests__/pages/add-hotel.test.tsx
import { describe, expect, it, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import AddHotelPage from '../../app/hotels/add/page';

// Mock the Next.js useRouter hook
const mockPush = vi.fn();
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush,
  }),
}));

describe('AddHotelPage', () => {
  beforeEach(() => {
    // Clear localStorage and mocks before each test
    localStorage.clear();
    mockPush.mockClear();
  });

  it('renders the add hotel form', () => {
    render(<AddHotelPage />);
    
    expect(screen.getByText('Add Hotel Information')).toBeTruthy();
    expect(screen.getByLabelText(/Hotel Name/i)).toBeTruthy();
    expect(screen.getByLabelText(/Price per Night/i)).toBeTruthy();
    expect(screen.getByLabelText(/Rating/i)).toBeTruthy();
    expect(screen.getByText(/Submit & Compare/i)).toBeTruthy();
  });

  it('shows validation errors for empty fields', async () => {
    render(<AddHotelPage />);
    
    // Submit the form without filling any fields
    const submitButton = screen.getByText(/Submit & Compare/i);
    await userEvent.click(submitButton);
    
    // Check if validation errors are displayed
    expect(screen.getByText(/Hotel name is required/i)).toBeTruthy();
    expect(screen.getByText(/Price must be a positive number/i)).toBeTruthy();
    expect(screen.getByText(/Rating must be between 0 and 10/i)).toBeTruthy();
  });

  it('validates field values appropriately', async () => {
    render(<AddHotelPage />);
    
    // Fill invalid values
    await userEvent.type(screen.getByLabelText(/Hotel Name/i), 'Test Hotel');
    await userEvent.type(screen.getByLabelText(/Price per Night/i), '-50');
    await userEvent.type(screen.getByLabelText(/Rating/i), '11');
    
    // Submit form
    const submitButton = screen.getByText(/Submit & Compare/i);
    await userEvent.click(submitButton);
    
    // Check validation errors
    expect(screen.queryByText(/Hotel name is required/i)).not.toBeTruthy();
    expect(screen.getByText(/Price must be a positive number/i)).toBeTruthy();
    expect(screen.getByText(/Rating must be between 0 and 10/i)).toBeTruthy();
  });

  it('successfully submits the form with valid data', async () => {
    render(<AddHotelPage />);
    
    // Fill valid form data
    await userEvent.type(screen.getByLabelText(/Hotel Name/i), 'Grand Hotel');
    await userEvent.type(screen.getByLabelText(/Price per Night/i), '150');
    await userEvent.type(screen.getByLabelText(/Rating/i), '8.5');
    
    // Select a currency
    await userEvent.selectOptions(screen.getByRole('combobox'), ['EUR']);
    
    // Submit form
    const submitButton = screen.getByText(/Submit & Compare/i);
    await userEvent.click(submitButton);
    
    // Check if hotels were saved to localStorage
    const savedHotels = JSON.parse(localStorage.getItem('hotels') || '[]');
    expect(savedHotels).toHaveLength(1);
    expect(savedHotels[0]).toEqual({
      name: 'Grand Hotel',
      price: 150,
      rating: 8.5,
      currency: 'EUR'
    });
    
    // Check if navigation occurred
    expect(mockPush).toHaveBeenCalledWith('/hotels/compare');
  });

  it('adds hotel to existing hotels in localStorage', async () => {
    // Setup existing hotels in localStorage
    const existingHotels = [
      { name: 'Existing Hotel', price: 100, rating: 7, currency: 'USD' }
    ];
    localStorage.setItem('hotels', JSON.stringify(existingHotels));
    
    render(<AddHotelPage />);

    // Fill valid form data
    await userEvent.type(screen.getByLabelText(/Hotel Name/i), 'New Hotel');
    await userEvent.type(screen.getByLabelText(/Price per Night/i), '200');
    await userEvent.type(screen.getByLabelText(/Rating/i), '9');
    
    // Submit form
    const submitButton = screen.getByText(/Submit & Compare/i);
    await userEvent.click(submitButton);
    
    // Check if both hotels were saved
    const savedHotels = JSON.parse(localStorage.getItem('hotels') || '[]');
    expect(savedHotels).toHaveLength(2);
    expect(savedHotels[1].name).toBe('New Hotel');
  });
});