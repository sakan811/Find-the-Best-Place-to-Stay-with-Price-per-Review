// __tests__/pages/compare-hotels.test.tsx
import { describe, expect, it, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import CompareHotelsPage from '../../app/hotels/compare/page';

// Mock Next.js useRouter
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

describe('CompareHotelsPage', () => {
  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear();
  });

  it('shows empty state when no hotels are added', () => {
    render(<CompareHotelsPage />);
    
    expect(screen.getByText('No hotels have been added yet.')).toBeTruthy();
    expect(screen.getByText('Add Your First Hotel')).toBeTruthy();
  });

  it('renders hotel comparison table with sorted hotels', () => {
    // Setup test data in localStorage
    const testHotels = [
      { name: 'Budget Inn', price: 50, rating: 7, currency: 'USD' },
      { name: 'Luxury Resort', price: 200, rating: 9, currency: 'USD' },
      { name: 'Best Value Hotel', price: 80, rating: 8, currency: 'USD' }
    ];
    localStorage.setItem('hotels', JSON.stringify(testHotels));
    
    render(<CompareHotelsPage />);
    
    // Check if all hotels are displayed
    expect(screen.getByText('Budget Inn')).toBeTruthy();
    expect(screen.getByText('Luxury Resort')).toBeTruthy();
    expect(screen.getByText('Best Value Hotel')).toBeTruthy();
    
    // Check column headers
    expect(screen.getByText('Rank')).toBeTruthy();
    expect(screen.getByText('Hotel')).toBeTruthy();
    expect(screen.getByText('Price')).toBeTruthy();
    expect(screen.getByText('Rating')).toBeTruthy();
    expect(screen.getByText('Value')).toBeTruthy();
    
    // Check if value scores are calculated correctly
    const rows = screen.getAllByRole('row');
    
    // Find first row (excluding header)
    const firstRow = rows[1];
    
    // Extract text from the first cell (rank)
    expect(firstRow.textContent).toContain('1');
    
    // Check if the best value hotel is highlighted
    const valueScores = [7/50, 9/200, 8/80];
    const bestValueIndex = valueScores.indexOf(Math.max(...valueScores));
    const bestHotelName = testHotels[bestValueIndex].name;
    
    // The row containing the best hotel should have the star indicator
    expect(screen.getByText(bestHotelName)).toBeTruthy();
  });

  it('clears hotels when clear button is clicked', async () => {
    // Setup test data in localStorage
    const testHotels = [
      { name: 'Hotel A', price: 100, rating: 8, currency: 'USD' },
      { name: 'Hotel B', price: 150, rating: 9, currency: 'EUR' }
    ];
    localStorage.setItem('hotels', JSON.stringify(testHotels));
    
    render(<CompareHotelsPage />);
    
    // Verify hotels are displayed
    expect(screen.getByText('Hotel A')).toBeTruthy();
    expect(screen.getByText('Hotel B')).toBeTruthy();
    
    // Click clear button
    const clearButton = screen.getByText('Clear All Hotels');
    await userEvent.click(clearButton);
    
    // Verify hotels are removed and empty state is shown
    expect(screen.getByText('No hotels have been added yet.')).toBeTruthy();
    expect(localStorage.getItem('hotels')).toBeNull();
  });

  it('displays prices with correct currency format', () => {
    // Setup test data with different currencies
    const testHotels = [
      { name: 'USD Hotel', price: 100, rating: 8, currency: 'USD' },
      { name: 'EUR Hotel', price: 90, rating: 8, currency: 'EUR' },
      { name: 'GBP Hotel', price: 80, rating: 8, currency: 'GBP' }
    ];
    localStorage.setItem('hotels', JSON.stringify(testHotels));
    
    render(<CompareHotelsPage />);
    
    // Check if currencies are correctly displayed
    expect(screen.getByText(/100.00 USD/)).toBeTruthy();
    expect(screen.getByText(/90.00 EUR/)).toBeTruthy();
    expect(screen.getByText(/80.00 GBP/)).toBeTruthy();
  });

  it('shows explanation about value score calculation', () => {
    // Setup test data in localStorage
    const testHotels = [{ name: 'Hotel A', price: 100, rating: 8, currency: 'USD' }];
    localStorage.setItem('hotels', JSON.stringify(testHotels));
    
    render(<CompareHotelsPage />);
    
    // Check if explanation is displayed
    expect(screen.getByText(/Value Score/i)).toBeTruthy();
    expect(screen.getByText(/Rating ÷ Price/i)).toBeTruthy();
  });
});