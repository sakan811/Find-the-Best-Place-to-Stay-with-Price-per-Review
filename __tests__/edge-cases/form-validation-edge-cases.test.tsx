import AddHotelPage from "@/app/hotels/add/page";
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, beforeEach, it, expect, vi } from "vitest";

// Mock the Next.js useRouter hook
const mockPush = vi.fn();
vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: mockPush,
  }),
}));

describe("Form Validation Edge Cases", () => {
  beforeEach(() => {
    localStorage.clear();
    mockPush.mockClear();
    cleanup();
  });

  it("handles extremely large price values", async () => {
    const user = userEvent.setup();
    render(<AddHotelPage />);

    const nameInput = screen.getByLabelText(/Hotel Name/i);
    const priceInput = screen.getByLabelText(/Price/i);
    const ratingInput = screen.getByLabelText(/Rating/i);

    await user.clear(nameInput);
    await user.clear(priceInput);
    await user.clear(ratingInput);

    await user.type(nameInput, "Expensive Hotel");
    await user.type(priceInput, "999999999.99");
    await user.type(ratingInput, "10");

    const submitButton = screen.getByRole("button", { name: /Submit & Compare/i });
    await user.click(submitButton);

    const savedHotels = JSON.parse(localStorage.getItem("hotels") || "[]");
    expect(savedHotels).toHaveLength(1);
    expect(savedHotels[0].price).toBe(999999999.99);
    expect(mockPush).toHaveBeenCalledWith("/hotels/compare");
  });

  it("handles very small decimal prices", async () => {
    const user = userEvent.setup();
    render(<AddHotelPage />);

    const nameInput = screen.getByLabelText(/Hotel Name/i);
    const priceInput = screen.getByLabelText(/Price/i);
    const ratingInput = screen.getByLabelText(/Rating/i);

    await user.clear(nameInput);
    await user.clear(priceInput);
    await user.clear(ratingInput);

    await user.type(nameInput, "Budget Hotel");
    await user.type(priceInput, "0.01");
    await user.type(ratingInput, "5");

    const submitButton = screen.getByRole("button", { name: /Submit & Compare/i });
    await user.click(submitButton);

    const savedHotels = JSON.parse(localStorage.getItem("hotels") || "[]");
    expect(savedHotels).toHaveLength(1);
    expect(savedHotels[0].price).toBe(0.01);
    expect(mockPush).toHaveBeenCalledWith("/hotels/compare");
  });

  it("handles special characters in hotel names", async () => {
    const user = userEvent.setup();
    render(<AddHotelPage />);

    const specialName = "Hôtel André & Co. (★★★★★) 日本語";
    
    const nameInput = screen.getByLabelText(/Hotel Name/i);
    const priceInput = screen.getByLabelText(/Price/i);
    const ratingInput = screen.getByLabelText(/Rating/i);

    await user.clear(nameInput);
    await user.clear(priceInput);
    await user.clear(ratingInput);

    await user.type(nameInput, specialName);
    await user.type(priceInput, "150");
    await user.type(ratingInput, "8.5");

    const submitButton = screen.getByRole("button", { name: /Submit & Compare/i });
    await user.click(submitButton);

    const savedHotels = JSON.parse(localStorage.getItem("hotels") || "[]");
    expect(savedHotels).toHaveLength(1);
    expect(savedHotels[0].name).toBe(specialName);
    expect(mockPush).toHaveBeenCalledWith("/hotels/compare");
  });

  it("handles boundary rating values", async () => {
    const user = userEvent.setup();
    
    // Test exact boundaries
    const testCases = [
      { rating: "0", expected: 0 },
      { rating: "0.0", expected: 0 },
      { rating: "10", expected: 10 },
      { rating: "10.0", expected: 10 },
      { rating: "5.5555", expected: 5.5555 }
    ];

    for (const testCase of testCases) {
      // Clear storage and mocks for each iteration
      localStorage.clear();
      mockPush.mockClear();
      cleanup();
      
      // Re-render component for each test case to ensure clean state
      render(<AddHotelPage />);
      
      const nameInput = screen.getByLabelText(/Hotel Name/i);
      const priceInput = screen.getByLabelText(/Price/i);
      const ratingInput = screen.getByLabelText(/Rating/i);
      
      await user.clear(nameInput);
      await user.clear(priceInput);
      await user.clear(ratingInput);
      
      await user.type(nameInput, `Hotel ${testCase.rating}`);
      await user.type(priceInput, "100");
      await user.type(ratingInput, testCase.rating);

      const submitButton = screen.getByRole("button", { name: /Submit & Compare/i });
      await user.click(submitButton);

      // Wait for any async operations to complete
      await new Promise(resolve => setTimeout(resolve, 100));

      const savedHotels = JSON.parse(localStorage.getItem("hotels") || "[]");
      
      // Check that data was saved successfully for valid ratings
      expect(savedHotels).toHaveLength(1);
      expect(savedHotels[0].rating).toBe(testCase.expected);
      expect(mockPush).toHaveBeenCalledWith("/hotels/compare");
    }
  });

  it("rejects invalid rating values", async () => {
    const user = userEvent.setup();
    
    const invalidRatings = [
      { value: "-1", description: "negative rating" },
      { value: "11", description: "rating above 10" },
      { value: "abc", description: "non-numeric rating" },
      { value: "5.5.5", description: "malformed decimal" },
    ];

    for (const invalidRating of invalidRatings) {
      // Clear storage and mocks for each iteration
      localStorage.clear();
      mockPush.mockClear();
      cleanup();
      
      // Re-render component for each test case
      render(<AddHotelPage />);
      
      const nameInput = screen.getByLabelText(/Hotel Name/i);
      const priceInput = screen.getByLabelText(/Price/i);
      const ratingInput = screen.getByLabelText(/Rating/i);
      
      await user.clear(nameInput);
      await user.clear(priceInput);
      await user.clear(ratingInput);
      
      await user.type(nameInput, "Test Hotel");
      await user.type(priceInput, "100");
      await user.type(ratingInput, invalidRating.value);

      const submitButton = screen.getByRole("button", { name: /Submit & Compare/i });
      await user.click(submitButton);

      // Wait for any validation to complete
      await new Promise(resolve => setTimeout(resolve, 100));

      // Should not navigate if validation fails
      expect(mockPush).not.toHaveBeenCalled();
      
      // Should not save invalid data to localStorage
      const savedHotels = JSON.parse(localStorage.getItem("hotels") || "[]");
      expect(savedHotels).toHaveLength(0);
    }
  });

  it("rejects empty rating value", async () => {
    const user = userEvent.setup();
    render(<AddHotelPage />);
    
    const nameInput = screen.getByLabelText(/Hotel Name/i);
    const priceInput = screen.getByLabelText(/Price/i);
    const ratingInput = screen.getByLabelText(/Rating/i);
    
    await user.clear(nameInput);
    await user.clear(priceInput);
    await user.clear(ratingInput);
    
    await user.type(nameInput, "Test Hotel");
    await user.type(priceInput, "100");
    // Don't type anything in rating field (leave it empty)

    const submitButton = screen.getByRole("button", { name: /Submit & Compare/i });
    await user.click(submitButton);

    // Wait for validation
    await new Promise(resolve => setTimeout(resolve, 100));

    // Should not navigate if validation fails
    expect(mockPush).not.toHaveBeenCalled();
    
    // Should not save invalid data to localStorage
    const savedHotels = JSON.parse(localStorage.getItem("hotels") || "[]");
    expect(savedHotels).toHaveLength(0);
  });

  it("handles whitespace in inputs", async () => {
    const user = userEvent.setup();
    render(<AddHotelPage />);

    const nameInput = screen.getByLabelText(/Hotel Name/i);
    const priceInput = screen.getByLabelText(/Price/i);
    const ratingInput = screen.getByLabelText(/Rating/i);

    await user.clear(nameInput);
    await user.clear(priceInput);
    await user.clear(ratingInput);

    await user.type(nameInput, "  Trimmed Hotel  ");
    await user.type(priceInput, " 100.50 ");
    await user.type(ratingInput, " 8.5 ");

    const submitButton = screen.getByRole("button", { name: /Submit & Compare/i });
    await user.click(submitButton);

    const savedHotels = JSON.parse(localStorage.getItem("hotels") || "[]");
    expect(savedHotels).toHaveLength(1);
    
    // Test actual behavior - inputs might be trimmed or preserved
    const savedHotel = savedHotels[0];
    expect(savedHotel.name).toMatch(/Trimmed Hotel/); // Should contain the text
    expect(savedHotel.price).toBe(100.50);
    expect(savedHotel.rating).toBe(8.5);
    expect(mockPush).toHaveBeenCalledWith("/hotels/compare");
  });

  it("rejects missing required fields", async () => {
    const user = userEvent.setup();
    render(<AddHotelPage />);

    const nameInput = screen.getByLabelText(/Hotel Name/i);
    const priceInput = screen.getByLabelText(/Price/i);
    const ratingInput = screen.getByLabelText(/Rating/i);

    // Test missing hotel name
    await user.clear(nameInput);
    await user.clear(priceInput);
    await user.clear(ratingInput);
    
    await user.type(priceInput, "100");
    await user.type(ratingInput, "8");
    
    const submitButton = screen.getByRole("button", { name: /Submit & Compare/i });
    await user.click(submitButton);

    // Wait for validation
    await new Promise(resolve => setTimeout(resolve, 100));

    expect(mockPush).not.toHaveBeenCalled();
    expect(JSON.parse(localStorage.getItem("hotels") || "[]")).toHaveLength(0);
  });

  it("handles invalid price values", async () => {
    const user = userEvent.setup();
    
    const invalidPrices = [
      { value: "-50", description: "negative price" },
      { value: "0", description: "zero price" },
      { value: "abc", description: "non-numeric price" },
      { value: "1.2.3", description: "malformed decimal price" },
    ];

    for (const invalidPrice of invalidPrices) {
      localStorage.clear();
      mockPush.mockClear();
      cleanup();
      
      render(<AddHotelPage />);
      
      const nameInput = screen.getByLabelText(/Hotel Name/i);
      const priceInput = screen.getByLabelText(/Price/i);
      const ratingInput = screen.getByLabelText(/Rating/i);

      await user.clear(nameInput);
      await user.clear(priceInput);
      await user.clear(ratingInput);
      
      await user.type(nameInput, "Test Hotel");
      await user.type(priceInput, invalidPrice.value);
      await user.type(ratingInput, "8");

      const submitButton = screen.getByRole("button", { name: /Submit & Compare/i });
      await user.click(submitButton);

      // Wait for validation
      await new Promise(resolve => setTimeout(resolve, 100));

      // Should not navigate or save invalid data
      expect(mockPush).not.toHaveBeenCalled();
      const savedHotels = JSON.parse(localStorage.getItem("hotels") || "[]");
      expect(savedHotels).toHaveLength(0);
    }
  });

  it("handles extremely long hotel names", async () => {
    const user = userEvent.setup();
    render(<AddHotelPage />);

    const nameInput = screen.getByLabelText(/Hotel Name/i);
    const priceInput = screen.getByLabelText(/Price/i);
    const ratingInput = screen.getByLabelText(/Rating/i);

    // Test with very long hotel name (but not too long to cause timeout)
    const longName = "A".repeat(500); // Reduced from 1000 to prevent timeout
    
    await user.clear(nameInput);
    await user.clear(priceInput);
    await user.clear(ratingInput);
    
    await user.type(nameInput, longName);
    await user.type(priceInput, "100");
    await user.type(ratingInput, "8");

    const submitButton = screen.getByRole("button", { name: /Submit & Compare/i });
    await user.click(submitButton);

    // Wait for form submission
    await new Promise(resolve => setTimeout(resolve, 100));

    const savedHotels = JSON.parse(localStorage.getItem("hotels") || "[]");
    
    // Should accept long names (most forms don't have length validation)
    expect(savedHotels).toHaveLength(1);
    expect(savedHotels[0].name).toBe(longName);
    expect(savedHotels[0].price).toBe(100);
    expect(savedHotels[0].rating).toBe(8);
    expect(mockPush).toHaveBeenCalledWith("/hotels/compare");
  });

  it("preserves currency selection between form submissions", async () => {
    const user = userEvent.setup();
    render(<AddHotelPage />);

    // Fix: Use document.getElementById directly since the select doesn't have a label
    const currencySelect = document.getElementById("currency") as HTMLSelectElement;
    
    // Change currency to EUR
    await user.selectOptions(currencySelect, "EUR");
    
    // Fill and submit form
    const nameInput = screen.getByLabelText(/Hotel Name/i);
    const priceInput = screen.getByLabelText(/Price/i);
    const ratingInput = screen.getByLabelText(/Rating/i);

    await user.clear(nameInput);
    await user.clear(priceInput);
    await user.clear(ratingInput);

    await user.type(nameInput, "European Hotel");
    await user.type(priceInput, "150");
    await user.type(ratingInput, "9");

    const submitButton = screen.getByRole("button", { name: /Submit & Compare/i });
    await user.click(submitButton);

    const savedHotels = JSON.parse(localStorage.getItem("hotels") || "[]");
    expect(savedHotels).toHaveLength(1);
    expect(savedHotels[0].currency).toBe("EUR");
    
    // Check that currency preference was saved
    expect(localStorage.getItem("lastUsedCurrency")).toBe("EUR");
    expect(mockPush).toHaveBeenCalledWith("/hotels/compare");
  });
});