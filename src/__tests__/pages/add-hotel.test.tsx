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
    
    expect(screen.getAllByText('Add Hotel Information')[0]).toBeTruthy();
    expect(screen.getAllByLabelText(/Hotel Name/i)[0]).toBeTruthy();
    expect(screen.getAllByLabelText(/Price/i)[0]).toBeTruthy();
    expect(screen.getAllByLabelText(/Rating/i)[0]).toBeTruthy();
    expect(screen.getAllByText(/Submit & Compare/i)[0]).toBeTruthy();
  });

  it('shows validation errors for empty fields', async () => {
    render(<AddHotelPage />);
    
    // Submit the form without filling any fields
    const submitButtons = screen.getAllByText(/Submit & Compare/i);
    await userEvent.click(submitButtons[0]);
    
    // Check that navigation did not occur
    expect(mockPush).not.toHaveBeenCalled();
    
    // Check that localStorage wasn't updated
    const savedHotels = JSON.parse(localStorage.getItem('hotels') || '[]');
    expect(savedHotels).toHaveLength(0);
  });

  it('validates field values appropriately', async () => {
    const user = userEvent.setup();
    render(<AddHotelPage />);
    
    // Get input fields and submit button
    const nameInput = screen.getAllByLabelText(/Hotel Name/i)[0];
    const priceInput = screen.getAllByLabelText(/Price/i)[0];
    const ratingInput = screen.getAllByLabelText(/Rating/i)[0];
    const submitButton = screen.getAllByText(/Submit & Compare/i)[0];
    
    // Enter valid name but invalid price and rating
    await user.type(nameInput, 'Test Hotel');
    await user.clear(priceInput);
    await user.type(priceInput, '-50');
    await user.type(ratingInput, '11');
    
    // Trigger validation by attempting submission
    await user.click(submitButton);

    // Check if validation was called and form submission was prevented
    expect(mockPush).not.toHaveBeenCalled();
    
    // Check that localStorage wasn't updated since validation failed
    const savedHotels = JSON.parse(localStorage.getItem('hotels') || '[]');
    expect(savedHotels).toHaveLength(0);
  });
  it('successfully submits the form with valid data and proper data types', async () => {
    const user = userEvent.setup();
    render(<AddHotelPage />);
    
    // Get input fields
    const nameInput = screen.getAllByLabelText(/Hotel Name/i)[0];
    const priceInput = screen.getAllByLabelText(/Price/i)[0];
    const ratingInput = screen.getAllByLabelText(/Rating/i)[0];
    const currencySelect = document.getElementById('currency') as HTMLSelectElement;
    const submitButton = screen.getAllByText(/Submit & Compare/i)[0];
    
    // Fill valid form data
    await user.clear(nameInput);
    await user.type(nameInput, 'Grand Hotel');
    await user.clear(priceInput);
    await user.type(priceInput, '150');
    await user.clear(ratingInput);
    await user.type(ratingInput, '8.5');
    await user.selectOptions(currencySelect, 'USD');

    // Mock localStorage.setItem
    const originalSetItem = localStorage.setItem;
    let savedData: string | null = null;
    localStorage.setItem = vi.fn((key, value) => {
      if (key === 'hotels') {
        savedData = value;
      }
      return originalSetItem.call(localStorage, key, value);
    });

    // Submit form
    await user.click(submitButton);

    // Wait for state updates
    await new Promise(resolve => setTimeout(resolve, 300));

    // Restore original localStorage.setItem
    localStorage.setItem = originalSetItem;    // Parse the saved data
    const savedHotels = savedData ? JSON.parse(savedData) : [];
    
    // Verify the expected hotel data was saved
    expect(savedHotels).toHaveLength(1);
    
    // Check if the last hotel added matches our test data with proper types
    const lastHotel = savedHotels[0];
    expect(lastHotel).toEqual({
      name: 'Grand Hotel',
      price: 150, // Should be number, not string
      rating: 8.5, // Should be number, not string
      currency: 'USD' // Default currency
    });
    
    // Check that navigation was called
    expect(mockPush).toHaveBeenCalledWith('/hotels/compare');
  });
  it('adds hotel to existing hotels in localStorage with currency', async () => {
    const user = userEvent.setup();
    
    // Setup existing hotels in localStorage
    const existingHotels = [
      { name: 'Existing Hotel', price: 100, rating: 7, currency: 'EUR' }
    ];
    localStorage.setItem('hotels', JSON.stringify(existingHotels));
    
    render(<AddHotelPage />);
    
    // Fill valid form data
    const nameInput = screen.getAllByLabelText(/Hotel Name/i)[0];
    const priceInput = screen.getAllByLabelText(/Price/i)[0];
    const ratingInput = screen.getAllByLabelText(/Rating/i)[0];
    const submitButton = screen.getAllByText(/Submit & Compare/i)[0];
    
    await user.clear(nameInput);
    await user.type(nameInput, 'New Hotel');
    await user.clear(priceInput);
    await user.type(priceInput, '200');
    await user.clear(ratingInput);
    await user.type(ratingInput, '9');
    
    // Change currency - get by id instead of role with name
    const currencySelect = document.getElementById('currency') as HTMLSelectElement;
    await user.selectOptions(currencySelect, 'EUR');
    
    // Mock localStorage.setItem
    const originalSetItem = localStorage.setItem;
    let savedData: string | null = null;
    localStorage.setItem = vi.fn((key, value) => {
      if (key === 'hotels') {
        savedData = value;
      }
      return originalSetItem.call(localStorage, key, value);
    });
    
    // Submit form
    await user.click(submitButton);
    
    // Wait for state updates
    await new Promise(resolve => setTimeout(resolve, 300));
    
    // Restore original localStorage.setItem
    localStorage.setItem = originalSetItem;
      // Parse the saved data
    const savedHotels = savedData ? JSON.parse(savedData) : [];
    
    // Verify the final localStorage state
    expect(savedHotels).toHaveLength(2);
    
    // Check if existing hotel was preserved
    expect(savedHotels[0]).toEqual({
      name: 'Existing Hotel',
      price: 100,
      rating: 7,
      currency: 'EUR'
    });
    
    // Check if the new hotel was added with correct types and currency
    expect(savedHotels[1]).toEqual({
      name: 'New Hotel',
      price: 200, // Should be number, not string
      rating: 9, // Should be number, not string
      currency: 'EUR'
    });
    
    // Check that navigation was called
    expect(mockPush).toHaveBeenCalledWith('/hotels/compare');
  });
});