import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import AddHotelPage from "../../src/app/hotels/add/page";
import CompareHotelsPage from "../../src/app/hotels/compare/page";

// Mock Next.js router
const mockPush = vi.fn();
vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: mockPush }),
}));

describe("localStorage Error Handling", () => {
  let originalLocalStorage: Storage;
  
  beforeEach(() => {
    originalLocalStorage = window.localStorage;
    mockPush.mockClear();
  });

  afterEach(() => {
    Object.defineProperty(window, 'localStorage', {
      value: originalLocalStorage,
      writable: true
    });
    cleanup();
  });

  it("handles corrupted JSON in localStorage gracefully", () => {
    // Mock localStorage with corrupted data
    const mockLocalStorage = {
      getItem: vi.fn(() => '{"malformed": json}'),
      setItem: vi.fn(),
      removeItem: vi.fn(),
      clear: vi.fn(),
    };
    
    Object.defineProperty(window, 'localStorage', {
      value: mockLocalStorage,
      writable: true
    });

    render(<CompareHotelsPage />);
    
    // Should show empty state instead of crashing
    expect(screen.getByText("No Hotels Added Yet")).toBeTruthy();
  });

  it("handles localStorage quota exceeded error", async () => {
    const user = userEvent.setup();
    
    // Mock localStorage that throws quota exceeded error
    const mockLocalStorage = {
      getItem: vi.fn(() => null),
      setItem: vi.fn(() => {
        throw new Error("QuotaExceededError");
      }),
      removeItem: vi.fn(),
      clear: vi.fn(),
    };
    
    Object.defineProperty(window, 'localStorage', {
      value: mockLocalStorage,
      writable: true
    });

    render(<AddHotelPage />);
    
    // Fill form with valid data
    await user.type(screen.getByLabelText(/Hotel Name/i), "Test Hotel");
    await user.type(screen.getByLabelText(/Price/i), "100");
    await user.type(screen.getByLabelText(/Rating/i), "8");
    
    // Submit should handle error gracefully
    await user.click(screen.getByText(/Submit & Compare/i));
    
    // Should not navigate if save failed
    expect(mockPush).not.toHaveBeenCalled();
  });

  it("handles unavailable localStorage", () => {
    // Remove localStorage entirely
    Object.defineProperty(window, 'localStorage', {
      value: undefined,
      writable: true
    });

    render(<CompareHotelsPage />);
    
    // Should show empty state gracefully
    expect(screen.getByText("No Hotels Added Yet")).toBeTruthy();
  });

  it("handles localStorage with mixed data types", () => {
    const mockLocalStorage = {
      getItem: vi.fn(() => JSON.stringify([
        { name: "Valid Hotel", price: 100, rating: 8, currency: "USD" },
        "invalid string entry",
        { name: "Missing Price", rating: 9, currency: "EUR" },
        { name: "Invalid Rating", price: 200, rating: "not a number", currency: "GBP" },
        null,
        undefined
      ])),
      setItem: vi.fn(),
      removeItem: vi.fn(),
      clear: vi.fn(),
    };
    
    Object.defineProperty(window, 'localStorage', {
      value: mockLocalStorage,
      writable: true
    });

    render(<CompareHotelsPage />);
    
    // Should only show valid hotels or handle gracefully
    // The component should filter out invalid entries
  });
});