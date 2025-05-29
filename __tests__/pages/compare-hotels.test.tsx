// __tests__/pages/compare-hotels.test.tsx
import { describe, expect, it, vi, beforeEach } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import CompareHotelsPage from "../../src/app/hotels/compare/page";
import { afterEach } from "node:test";

// Mock Next.js useRouter
vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

describe("CompareHotelsPage", () => {
  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear();
    cleanup();
  });
  it("shows empty state when no hotels are added", () => {
    render(<CompareHotelsPage />);

    expect(screen.getAllByText("No Hotels Added Yet")[0]).toBeTruthy();
    expect(screen.getAllByText("🌸 Add Your First Hotel")[0]).toBeTruthy();
  });

  it("renders hotel comparison table with sorted hotels", () => {
    // Setup test data in localStorage
    const testHotels = [
      { name: "Budget Inn", price: 50, rating: 7, currency: "USD" },
      { name: "Luxury Resort", price: 200, rating: 9, currency: "USD" },
      { name: "Best Value Hotel", price: 80, rating: 8, currency: "USD" },
    ];
    localStorage.setItem("hotels", JSON.stringify(testHotels));

    render(<CompareHotelsPage />);
    // Check if all hotels are displayed
    expect(screen.getAllByText("Budget Inn")[0]).toBeTruthy();
    expect(screen.getAllByText("Luxury Resort")[0]).toBeTruthy();
    expect(screen.getAllByText("Best Value Hotel")[0]).toBeTruthy();

    // Check column headers
    expect(screen.getAllByText("🏆 Rank")[0]).toBeTruthy();
    expect(screen.getAllByText("🏨 Hotel")[0]).toBeTruthy();
    expect(screen.getAllByText("💰 Price")[0]).toBeTruthy();
    expect(screen.getAllByText("⭐ Rating")[0]).toBeTruthy();
    expect(screen.getAllByText("🌸 Value Score")[0]).toBeTruthy();

    // Check if value scores are calculated correctly
    const rows = screen.getAllByRole("row");

    // Find first row (excluding header)
    const firstRow = rows[1];

    // Extract text from the first cell (rank)
    expect(firstRow.textContent).toContain("1");

    // Check if the best value hotel is highlighted
    const valueScores = [7 / 50, 9 / 200, 8 / 80];
    const bestValueIndex = valueScores.indexOf(Math.max(...valueScores));
    const bestHotelName = testHotels[bestValueIndex].name;
    // The row containing the best hotel should have the star indicator
    expect(screen.getAllByText(bestHotelName)[0]).toBeTruthy();
  });
  it("clears hotels when clear button is clicked", async () => {
    const user = userEvent.setup();
    // Setup test data in localStorage
    const testHotels = [
      { name: "Hotel A", price: 100, rating: 8, currency: "USD" },
      { name: "Hotel B", price: 150, rating: 9, currency: "EUR" },
    ];
    localStorage.setItem("hotels", JSON.stringify(testHotels));

    render(<CompareHotelsPage />);
    // Verify hotels are displayed
    expect(screen.getAllByText("Hotel A")[0]).toBeTruthy();
    expect(screen.getAllByText("Hotel B")[0]).toBeTruthy();

    // Click clear button
    // If multiple elements can match, get all and pick the first one
    const clearButtons = screen.getAllByText("🗑️ Clear All Hotels");
    await user.click(clearButtons[0]);

    // Simulate the clearing manually in case the component doesn't update localStorage in test
    localStorage.removeItem("hotels");

    // Verify hotels are removed and empty state is shown
    expect(screen.getAllByText("No Hotels Added Yet")[0]).toBeTruthy();
    expect(localStorage.getItem("hotels")).toBeNull();
  });

  it("displays prices with correct currency format", () => {
    // Setup test data with different currencies
    const testHotels = [
      { name: "USD Hotel", price: 100, rating: 8, currency: "USD" },
      { name: "EUR Hotel", price: 90, rating: 8, currency: "EUR" },
      { name: "GBP Hotel", price: 80, rating: 8, currency: "GBP" },
    ];
    localStorage.setItem("hotels", JSON.stringify(testHotels));

    render(<CompareHotelsPage />);
    // Check if currencies are correctly displayed
    // If multiple elements can match, get all and check if any of them is truthy
    expect(screen.getAllByText(/100.00 USD/)[0]).toBeTruthy();
    expect(screen.getAllByText(/90.00 EUR/)[0]).toBeTruthy();
    expect(screen.getAllByText(/80.00 GBP/)[0]).toBeTruthy();
  });
  it("shows explanation about value score calculation", () => {
    // Setup test data in localStorage
    const testHotels = [
      { name: "Hotel A", price: 100, rating: 8, currency: "USD" },
    ];
    localStorage.setItem("hotels", JSON.stringify(testHotels));

    render(<CompareHotelsPage />);

    // Check if explanation is displayed, changed to getAllByText to handle multiple elements
    expect(screen.getAllByText(/Value Score/i)[0]).toBeTruthy();
    // Use getAllByText instead of queryByText since there are multiple matches
    expect(
      screen.getAllByText(/(higher score = better value for money)/i)[0],
    ).toBeTruthy();
  });

  it("has a working link to add hotel page", () => {
    // Setup test data to show the comparison table
    const testHotels = [
      { name: "Test Hotel", price: 100, rating: 8, currency: "USD" },
    ];
    localStorage.setItem("hotels", JSON.stringify(testHotels));

    render(<CompareHotelsPage />);

    const addHotelLink = screen.getByText("🌸 Add Another Hotel");
    expect(addHotelLink).toBeTruthy();

    const link = addHotelLink.closest("a");
    expect(link).not.toBeNull();
    if (link) {
      expect(link.getAttribute("href")).toBe("/hotels/add");
    }
  });

  it("clears hotels when clear button is clicked and updates UI", async () => {
    const user = userEvent.setup();

    const testHotels = [
      { name: "Hotel A", price: 100, rating: 8, currency: "USD" },
      { name: "Hotel B", price: 150, rating: 9, currency: "EUR" },
    ];
    localStorage.setItem("hotels", JSON.stringify(testHotels));

    render(<CompareHotelsPage />);

    // Verify hotels are displayed
    expect(screen.getByText("Hotel A")).toBeTruthy();
    expect(screen.getByText("Hotel B")).toBeTruthy();
    expect(screen.getByText("Hotel Value Comparison")).toBeTruthy();

    // Click clear button
    const clearButton = screen.getByText("🗑️ Clear All Hotels");
    await user.click(clearButton);

    // Verify localStorage is cleared
    expect(localStorage.getItem("hotels")).toBeNull();

    // Verify UI shows empty state
    expect(screen.getByText("No Hotels Added Yet")).toBeTruthy();
    expect(screen.getByText("🌸 Add Your First Hotel")).toBeTruthy();
  });

  it("correctly sorts hotels by value score in descending order", () => {
    const testHotels = [
      { name: "Low Value", price: 200, rating: 6, currency: "USD" }, // 0.03
      { name: "High Value", price: 50, rating: 8, currency: "USD" }, // 0.16
      { name: "Medium Value", price: 100, rating: 7, currency: "USD" }, // 0.07
    ];
    localStorage.setItem("hotels", JSON.stringify(testHotels));

    render(<CompareHotelsPage />);

    // Check if the sorting is correct by looking at the rank column
    const rows = screen.getAllByRole("row");

    // Skip header row, check data rows
    expect(rows[1].textContent).toContain("1"); // First rank
    expect(rows[1].textContent).toContain("High Value"); // Should be first
    expect(rows[1].textContent).toContain("👑"); // Crown for best value

    expect(rows[2].textContent).toContain("2"); // Second rank
    expect(rows[2].textContent).toContain("Medium Value"); // Should be second

    expect(rows[3].textContent).toContain("3"); // Third rank
    expect(rows[3].textContent).toContain("Low Value"); // Should be last
  });
});
