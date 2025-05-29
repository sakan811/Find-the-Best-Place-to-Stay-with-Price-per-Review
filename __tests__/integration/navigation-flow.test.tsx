import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, cleanup } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import Home from "../../src/app/page";
import AddHotelPage from "../../src/app/hotels/add/page";
import CompareHotelsPage from "../../src/app/hotels/compare/page";

// Mock Next.js navigation
const mockPush = vi.fn();
vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: mockPush,
  }),
}));

// Mock Next.js Link component
vi.mock("next/link", () => ({
  default: ({
    children,
    href,
    className,
    ...props
  }: {
    children: React.ReactNode;
    href: string;
    className?: string;
    [key: string]: any;
  }) => (
    <a href={href} className={className} data-testid="mock-link" {...props}>
      {children}
    </a>
  ),
}));

describe("Navigation Flow Integration", () => {
  beforeEach(() => {
    localStorage.clear();
    mockPush.mockClear();
  });

  afterEach(() => {
    cleanup();
  });

  it("supports complete user journey: home -> add -> compare -> add again", async () => {
    const user = userEvent.setup();

    // ===== TEST HOME PAGE NAVIGATION =====
    render(<Home />);
    const addHotelLink = screen.getByText("🌸 Add a Hotel");
    expect(addHotelLink.closest("a")).toHaveAttribute("href", "/hotels/add");

    const compareLink = screen.getByText("Compare Hotels");
    expect(compareLink.closest("a")).toHaveAttribute("href", "/hotels/compare");
    cleanup();

    // ===== TEST ADD HOTEL PAGE FUNCTIONALITY =====
    render(<AddHotelPage />);

    // Fill and submit form
    const nameInput = screen.getByLabelText(/Hotel Name/i);
    const priceInput = screen.getByLabelText(/Price/i);
    const ratingInput = screen.getByLabelText(/Rating/i);

    await user.clear(nameInput);
    await user.type(nameInput, "Test Hotel");
    await user.clear(priceInput);
    await user.type(priceInput, "100");
    await user.clear(ratingInput);
    await user.type(ratingInput, "8");

    // Verify compare page link exists
    const comparePageLink = screen.getByText("View Compare Page");
    expect(comparePageLink.closest("a")).toHaveAttribute(
      "href",
      "/hotels/compare",
    );

    // Submit form
    const submitButton = screen.getByText(/Submit & Compare/i);
    await user.click(submitButton);

    // Check that navigation was called
    expect(mockPush).toHaveBeenCalledWith("/hotels/compare");
    cleanup();

    // ===== TEST COMPARE PAGE WITH DATA =====
    // Manually set up the localStorage data as if the form was submitted
    const testHotels = [
      { name: "Test Hotel", price: 100, rating: 8, currency: "USD" },
    ];
    localStorage.setItem("hotels", JSON.stringify(testHotels));

    render(<CompareHotelsPage />);

    // Verify hotel is displayed
    expect(screen.getByText("Test Hotel")).toBeTruthy();
    expect(screen.getByText("Hotel Value Comparison")).toBeTruthy();

    // Verify add another hotel link
    const addAnotherLinks = screen.getAllByText("🌸 Add Another Hotel");
    expect(addAnotherLinks[0].closest("a")).toHaveAttribute(
      "href",
      "/hotels/add",
    );

    // Test clear functionality
    const clearButton = screen.getByText("🗑️ Clear All Hotels");
    await user.click(clearButton);

    expect(screen.getByText("No Hotels Added Yet")).toBeTruthy();
    expect(screen.getByText("🌸 Add Your First Hotel")).toBeTruthy();
    cleanup();
  });

  it("handles empty state navigation properly", () => {
    // Test compare page with no data
    render(<CompareHotelsPage />);

    expect(screen.getByText("No Hotels Added Yet")).toBeTruthy();
    const addFirstHotelLink = screen.getByText("🌸 Add Your First Hotel");
    expect(addFirstHotelLink.closest("a")).toHaveAttribute(
      "href",
      "/hotels/add",
    );
  });

  it("validates form data persistence across navigation", async () => {
    const user = userEvent.setup();

    // Add first hotel
    render(<AddHotelPage />);

    const nameInput = screen.getByLabelText(/Hotel Name/i);
    const priceInput = screen.getByLabelText(/Price/i);
    const ratingInput = screen.getByLabelText(/Rating/i);

    await user.clear(nameInput);
    await user.type(nameInput, "First Hotel");
    await user.clear(priceInput);
    await user.type(priceInput, "150");
    await user.clear(ratingInput);
    await user.type(ratingInput, "9");

    const submitButton = screen.getByText(/Submit & Compare/i);
    await user.click(submitButton);

    // Verify data was saved to localStorage
    const savedHotels = JSON.parse(localStorage.getItem("hotels") || "[]");
    expect(savedHotels).toHaveLength(1);
    expect(savedHotels[0]).toEqual({
      name: "First Hotel",
      price: 150,
      rating: 9,
      currency: "USD",
    });
    cleanup();

    // Now test that compare page shows the data
    render(<CompareHotelsPage />);
    expect(screen.getByText("First Hotel")).toBeTruthy();
    expect(screen.getByText(/150\.00 USD/)).toBeTruthy();
    expect(screen.getByText("9.0")).toBeTruthy();
  });

  it("handles currency selection across navigation", async () => {
    const user = userEvent.setup();

    // Set a currency preference
    localStorage.setItem("lastUsedCurrency", "EUR");

    render(<AddHotelPage />);

    // Check if the saved currency is selected
    const currencySelect = document.getElementById(
      "currency",
    ) as HTMLSelectElement;
    expect(currencySelect.value).toBe("EUR");

    // Add hotel with EUR currency
    const nameInput = screen.getByLabelText(/Hotel Name/i);
    const priceInput = screen.getByLabelText(/Price/i);
    const ratingInput = screen.getByLabelText(/Rating/i);

    await user.clear(nameInput);
    await user.type(nameInput, "Euro Hotel");
    await user.clear(priceInput);
    await user.type(priceInput, "120");
    await user.clear(ratingInput);
    await user.type(ratingInput, "8.5");

    const submitButton = screen.getByText(/Submit & Compare/i);
    await user.click(submitButton);
    cleanup();

    // Verify currency is preserved in compare page
    render(<CompareHotelsPage />);
    expect(screen.getByText(/120\.00 EUR/)).toBeTruthy();
  });

  it("tests complete multi-hotel comparison workflow", async () => {
    const user = userEvent.setup();

    // Add multiple hotels to localStorage
    const multipleHotels = [
      { name: "Budget Hotel", price: 80, rating: 7, currency: "USD" }, // 7/80 = 0.0875
      { name: "Luxury Hotel", price: 300, rating: 9.5, currency: "USD" }, // 9.5/300 = 0.0317
      { name: "Mid Range", price: 150, rating: 8.5, currency: "USD" }, // 8.5/150 = 0.0567
    ];
    localStorage.setItem("hotels", JSON.stringify(multipleHotels));

    render(<CompareHotelsPage />);

    // Check all hotels are displayed
    expect(screen.getByText("Budget Hotel")).toBeTruthy();
    expect(screen.getByText("Luxury Hotel")).toBeTruthy();
    expect(screen.getByText("Mid Range")).toBeTruthy();

    // Check sorting - Budget Hotel should be first (highest value score)
    const rows = screen.getAllByRole("row");
    const firstDataRow = rows[1]; // Skip header row
    expect(firstDataRow.textContent).toContain("Budget Hotel");
    expect(firstDataRow.textContent).toContain("👑"); // Crown for best value

    // Test that value scores are displayed
    expect(screen.getByText("0.0875")).toBeTruthy(); // Budget Hotel value score

    // Test navigation to add more hotels
    const addAnotherLinks = screen.getAllByText("🌸 Add Another Hotel");
    expect(addAnotherLinks[0].closest("a")).toHaveAttribute(
      "href",
      "/hotels/add",
    );
  });
});
