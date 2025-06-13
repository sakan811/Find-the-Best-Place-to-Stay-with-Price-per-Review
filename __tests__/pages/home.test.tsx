import { describe, it, expect, vi, afterEach } from "vitest";
import { render, screen, cleanup } from "@testing-library/react";
import Home from "../../src/app/page";

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

describe("Home Page", () => {
  afterEach(() => {
    cleanup();
  });

  it("renders the hero section with correct title parts", () => {
    render(<Home />);

    // Test both parts of the title since they're in separate elements
    expect(screen.getByText("Find the Best Value Hotels")).toBeTruthy();
    expect(screen.getByText("with SakuYado")).toBeTruthy();
  });

  it("renders the description text", () => {
    render(<Home />);
    const descriptionElement = screen.getByText(
      /Compare hotels based on review-per-price ratio to get the most value for your money/,
    );
    expect(descriptionElement).toBeTruthy();
  });

  // ✅ Enhanced: Test both navigation buttons
  it("includes a link to add hotels with correct href", () => {
    render(<Home />);
    const addLink = screen.getByText("🌸 Add a Hotel");
    expect(addLink).toBeTruthy();

    const link = addLink.closest("a");
    expect(link).not.toBeNull();
    if (link) {
      expect(link.getAttribute("href")).toBe("/hotels/add");
    }
  });

  // ✅ NEW: Test compare hotels button
  it("includes a link to compare hotels with correct href", () => {
    render(<Home />);
    const compareLink = screen.getByText("Compare Hotels");
    expect(compareLink).toBeTruthy();

    const link = compareLink.closest("a");
    expect(link).not.toBeNull();
    if (link) {
      expect(link.getAttribute("href")).toBe("/hotels/compare");
    }
  });

  it("has the correct UI layout and styling", () => {
    render(<Home />);

    // Find the title by one of its parts
    const titleElement = screen.getByText("Find the Best Value Hotels");
    const heroSection = titleElement.closest("section");

    expect(heroSection).not.toBeNull();
    if (heroSection) {
      expect(heroSection.classList.contains("relative")).toBe(true);
      // Check for the correct gradient classes
      expect(heroSection.classList.contains("bg-gradient-to-br")).toBe(true);
      expect(heroSection.classList.contains("from-pink-500")).toBe(true);
    }
  });

  it("displays sakura emoji decorations", () => {
    render(<Home />);

    // Check for sakura emojis in the hero section
    const heroSection = document.querySelector("section");
    expect(heroSection).not.toBeNull();

    // The hero section should contain sakura emojis as decorative elements
    if (heroSection) {
      expect(heroSection.textContent).toContain("🌸");
    }
  });

  it("has proper responsive design classes", () => {
    render(<Home />);

    const titleElement = screen.getByText("Find the Best Value Hotels");
    expect(titleElement.classList.contains("text-3xl")).toBe(true);
    // Fix: Check for the actual responsive classes used in the component
    // Based on the component: "text-3xl sm:text-4xl md:text-5xl lg:text-6xl"
    expect(titleElement.classList.contains("sm:text-4xl")).toBe(true);
    expect(titleElement.classList.contains("md:text-5xl")).toBe(true);
    expect(titleElement.classList.contains("lg:text-6xl")).toBe(true);

    // Check button container has responsive classes
    const addButton = screen.getByText("🌸 Add a Hotel");
    const buttonContainer = addButton.closest("div");

    // The button container should have flex classes for responsive layout
    let hasFlexClasses = false;
    let currentElement = buttonContainer;

    while (currentElement && !hasFlexClasses) {
      if (currentElement.classList.contains("flex")) {
        hasFlexClasses = true;
      }
      currentElement = currentElement.parentElement;
    }

    expect(hasFlexClasses).toBe(true);
  });

  it("has proper button styling and hover effects", () => {
    render(<Home />);

    const addButton = screen.getByText("🌸 Add a Hotel");
    const compareButton = screen.getByText("Compare Hotels");

    // Get the actual link elements (closest 'a' tag)
    const addLink = addButton.closest("a");
    const compareLink = compareButton.closest("a");

    // Check add button styling
    expect(addLink).not.toBeNull();
    if (addLink) {
      expect(addLink.classList.contains("bg-white")).toBe(true);
      expect(addLink.classList.contains("text-pink-600")).toBe(true);
      expect(addLink.classList.contains("hover:bg-pink-50")).toBe(true);
    }

    // Check compare button styling
    expect(compareLink).not.toBeNull();
    if (compareLink) {
      expect(compareLink.classList.contains("bg-pink-600")).toBe(true);
      expect(compareLink.classList.contains("text-white")).toBe(true);
      expect(compareLink.classList.contains("hover:bg-pink-700")).toBe(true);
    }
  });
});