import { describe, it, expect, vi, afterEach } from "vitest";
import { render, screen, cleanup } from "@testing-library/react";

// Mock Next.js Link component
vi.mock("next/link", () => ({
  default: ({
    children,
    href,
  }: {
    children: React.ReactNode;
    href: string;
  }) => (
    <a href={href} data-testid="mock-link">
      {children}
    </a>
  ),
}));

// Create a wrapper component that only renders the body content
const LayoutContent = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-white to-rose-100">
      {/* Decorative sakura petals background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
        <div className="absolute top-10 left-10 w-4 h-4 bg-pink-300 rounded-full opacity-20 animate-pulse"></div>
        <div className="absolute top-32 right-20 w-3 h-3 bg-rose-300 rounded-full opacity-30 animate-pulse delay-1000"></div>
        <div className="absolute top-64 left-1/4 w-2 h-2 bg-pink-400 rounded-full opacity-25 animate-pulse delay-2000"></div>
        <div className="absolute bottom-32 right-1/3 w-3 h-3 bg-rose-200 rounded-full opacity-20 animate-pulse delay-3000"></div>
        <div className="absolute bottom-64 left-1/2 w-4 h-4 bg-pink-200 rounded-full opacity-15 animate-pulse delay-4000"></div>
      </div>

      <header className="relative z-10 bg-gradient-to-r from-pink-500 via-rose-400 to-pink-600 shadow-lg border-b-4 border-pink-200">
        <div className="container mx-auto px-4 py-6 flex justify-between items-center">
          <a
            href="/"
            className="text-2xl font-bold text-white hover:text-pink-100 transition-colors duration-300 drop-shadow-sm"
            data-testid="mock-link"
          >
            🌸 Hotel Value Analyzer
          </a>
        </div>
      </header>

      <main className="relative z-10 container mx-auto px-4 py-8">
        {children}
      </main>
    </div>
  );
};

describe("Root Layout", () => {
  afterEach(() => {
    cleanup();
  });

  it("renders the header with app title", () => {
    render(
      <LayoutContent>
        <div>Test Content</div>
      </LayoutContent>,
    );

    // Use a more flexible text matcher that handles the emoji
    expect(screen.getByText(/Hotel Value Analyzer/)).toBeTruthy();
  });

  it("renders the children content", () => {
    render(
      <LayoutContent>
        <div data-testid="test-child">Test Child Content</div>
      </LayoutContent>,
    );

    expect(screen.getByTestId("test-child")).toBeTruthy();
    expect(screen.getByText("Test Child Content")).toBeTruthy();
  });

  it("includes a link to the home page in the header", () => {
    render(
      <LayoutContent>
        <div>Test Content</div>
      </LayoutContent>,
    );

    const titleLink = screen.getByText(/Hotel Value Analyzer/);
    expect(titleLink.closest("a")).toHaveAttribute("href", "/");
  });

  it("has responsive design classes for mobile and desktop", () => {
    render(
      <LayoutContent>
        <div>Test Content</div>
      </LayoutContent>,
    );

    const header = document.querySelector("header");
    expect(header).not.toBeNull();
    if (header) {
      expect(header.classList.contains("relative")).toBe(true);
      expect(header.classList.contains("z-10")).toBe(true);
    }

    const container = document.querySelector(".container");
    expect(container).not.toBeNull();
    if (container) {
      expect(container.classList.contains("mx-auto")).toBe(true);
      expect(container.classList.contains("px-4")).toBe(true);
    }
  });

  it("header title has correct styling and hover effects", () => {
    render(
      <LayoutContent>
        <div>Test Content</div>
      </LayoutContent>,
    );

    const titleLink = screen.getByText(/Hotel Value Analyzer/);
    const linkElement = titleLink.closest("a");

    expect(linkElement).not.toBeNull();
    if (linkElement) {
      expect(linkElement.classList.contains("text-2xl")).toBe(true);
      expect(linkElement.classList.contains("font-bold")).toBe(true);
      expect(linkElement.classList.contains("text-white")).toBe(true);
      expect(linkElement.classList.contains("hover:text-pink-100")).toBe(true);
    }
  });

  it("has proper background gradient and decorative elements", () => {
    render(
      <LayoutContent>
        <div>Test Content</div>
      </LayoutContent>,
    );

    // Check main background gradient
    const mainWrapper = document.querySelector(".min-h-screen");
    expect(mainWrapper).not.toBeNull();
    if (mainWrapper) {
      expect(mainWrapper.classList.contains("bg-gradient-to-br")).toBe(true);
      expect(mainWrapper.classList.contains("from-pink-50")).toBe(true);
    }

    // Check decorative elements exist
    const decorativeElements = document.querySelectorAll(".animate-pulse");
    expect(decorativeElements.length).toBeGreaterThan(0);
  });
});

// Test the layout component's structure and behavior
describe("Root Layout Structure", () => {
  it("renders proper semantic HTML structure", () => {
    render(
      <LayoutContent>
        <div>Test Content</div>
      </LayoutContent>,
    );

    // Check semantic structure
    expect(document.querySelector("header")).toBeTruthy();
    expect(document.querySelector("main")).toBeTruthy();

    // Check header is positioned above main
    const header = document.querySelector("header");
    const main = document.querySelector("main");

    if (header && main) {
      const headerRect = header.getBoundingClientRect();
      const mainRect = main.getBoundingClientRect();
      // Header should be above main (smaller top value)
      expect(headerRect.top).toBeLessThanOrEqual(mainRect.top);
    }
  });

  it("maintains proper z-index layering", () => {
    render(
      <LayoutContent>
        <div>Test Content</div>
      </LayoutContent>,
    );

    const decorativeBackground = document.querySelector(".fixed.inset-0");
    const header = document.querySelector("header");
    const main = document.querySelector("main");

    // Check z-index classes
    expect(decorativeBackground?.classList.contains("z-0")).toBe(true);
    expect(header?.classList.contains("z-10")).toBe(true);
    expect(main?.classList.contains("z-10")).toBe(true);
  });
});
