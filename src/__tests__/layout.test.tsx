// __tests__/layout.test.tsx
import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import RootLayout from "../app/layout";

vi.mock("../app/globals.css", () => ({}));

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

describe("Root Layout", () => {
  it("renders the header with app title", () => {
    render(
      <RootLayout>
        <div>Test Content</div>
      </RootLayout>,
    );

    expect(screen.getAllByText("Hotel Value Analyzer")[0]).toBeTruthy();
  });

  it("renders the children content", () => {
    render(
      <RootLayout>
        <div data-testid="test-child">Test Child Content</div>
      </RootLayout>,
    );

    expect(screen.getByTestId("test-child")).toBeTruthy();
    expect(screen.getByText("Test Child Content")).toBeTruthy();
  });

  it("has proper HTML structure with language attribute", () => {
    render(
      <RootLayout>
        <div>Test Content</div>
      </RootLayout>,
    );

    const html = document.querySelector("html");
    expect(html).toHaveAttribute("lang", "en");
  });

  it("includes a link to the home page in the header", () => {
    render(
      <RootLayout>
        <div>Test Content</div>
      </RootLayout>,
    );

    const titleLink = screen.getAllByText("Hotel Value Analyzer");
    expect(titleLink[0].closest("a")).toHaveAttribute("href", "/");
  });
});
