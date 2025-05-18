// __tests__/pages/home.test.tsx
import { describe, it, expect, vi, afterEach } from 'vitest';
import { render, screen, cleanup } from '@testing-library/react';
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
  // Clean up after each test to ensure a fresh DOM
  afterEach(() => {
    cleanup();
  });
  
  it('renders the hero section with correct title', () => {
    render(<Home />);
    const titleElement = screen.getByText('Find the Best Value Hotels for Your Stay');
    expect(titleElement).toBeTruthy();
  });

  it('renders the description text', () => {
    render(<Home />);
    const descriptionElement = screen.getByText('Compare hotels based on review-per-price ratio to get the most value for your money');
    expect(descriptionElement).toBeTruthy();
  });

  it('includes a link to add hotels', () => {
    render(<Home />);
    const addLink = screen.getByText('Add a Hotel');
    expect(addLink).toBeTruthy();
    
    const link = addLink.closest('a');
    expect(link).not.toBeNull();
    if (link) {
      expect(link.getAttribute('href')).toBe('/hotels/add');
    }
  });

  it('has the correct UI layout and styling', () => {
    render(<Home />);
    const titleElement = screen.getByText('Find the Best Value Hotels for Your Stay');
    const heroSection = titleElement.closest('section');
    expect(heroSection).not.toBeNull();
    if (heroSection) {
      expect(heroSection.classList.contains('relative')).toBe(true);
      expect(heroSection.classList.contains('bg-blue-600')).toBe(true);
    }
    
    // Check for button styling
    const button = screen.getByText('Add a Hotel');
    const buttonLink = button.closest('a');
    expect(buttonLink).not.toBeNull();
    if (buttonLink) {
      expect(buttonLink.getAttribute('href')).toBe('/hotels/add');
    }
  });
});