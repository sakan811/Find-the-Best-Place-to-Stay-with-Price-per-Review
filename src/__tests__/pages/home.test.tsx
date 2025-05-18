// __tests__/pages/home.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import Home from '../../app/page';

// Mock Next.js Link component
vi.mock('next/link', () => ({
  default: ({ children, href }: { children: React.ReactNode, href: string }) => (
    <a href={href} data-testid="mock-link">
      {children}
    </a>
  ),
}));

describe('Home Page', () => {
  it('renders the hero section with correct title', () => {
    render(<Home />);
    
    expect(screen.getByText('Find the Best Value Hotels for Your Stay')).toBeTruthy();
  });

  it('renders the description text', () => {
    render(<Home />);
    
    expect(screen.getByText('Compare hotels based on review-per-price ratio to get the most value for your money')).toBeInTheDocument();
  });

  it('includes a link to add hotels', () => {
    render(<Home />);
    
    const addLink = screen.getByText('Add a Hotel');
    expect(addLink).toBeTruthy();
    expect(addLink.closest('a')).toHaveAttribute('href', '/hotels/add');
  });

  it('has the correct UI layout and styling', () => {
    render(<Home />);
    
    // Check for hero section
    const heroSection = screen.getByText('Find the Best Value Hotels for Your Stay').closest('section');
    expect(heroSection).toHaveClass('relative');
    expect(heroSection).toHaveClass('bg-blue-600');
    
    // Check for button styling
    const button = screen.getByText('Add a Hotel');
    expect(button.closest('a')).toHaveClass('bg-white');
    expect(button.closest('a')).toHaveClass('text-blue-600');
  });
});