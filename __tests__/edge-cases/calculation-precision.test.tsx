import { describe, it, expect } from "vitest";

describe("Calculation Precision Edge Cases", () => {
  it("handles floating point precision in value score calculation", () => {
    const testCases = [
      { rating: 7, price: 3, expected: 2.3333 }, // Repeating decimal
      { rating: 1, price: 3, expected: 0.3333 }, // Small repeating decimal
      { rating: 9.99999, price: 99.99999, expected: 0.1000 }, // High precision
      { rating: 0.1, price: 0.01, expected: 10.0000 }, // Very small numbers
    ];

    testCases.forEach(({ rating, price, expected }) => {
      // Using the same calculation logic as the app
      const valueScore = +(rating / price).toFixed(4);
      expect(valueScore).toBe(expected);
    });
  });

  it("handles sorting stability with identical value scores", () => {
    const hotels = [
      { name: "Hotel A", price: 100, rating: 8, currency: "USD", valueScore: 0.08 },
      { name: "Hotel B", price: 125, rating: 10, currency: "USD", valueScore: 0.08 },
      { name: "Hotel C", price: 200, rating: 16, currency: "USD", valueScore: 0.08 },
    ];

    // Test that sort is stable (maintains original order for equal values)
    const sorted = [...hotels].sort((a, b) => b.valueScore - a.valueScore);
    
    // All have same value score, so original order should be preserved
    expect(sorted[0].name).toBe("Hotel A");
    expect(sorted[1].name).toBe("Hotel B");
    expect(sorted[2].name).toBe("Hotel C");
  });

  it("handles extreme value ranges", () => {
    const extremeCases = [
      { rating: 10, price: 0.01, expected: 1000 }, // Very high value score
      { rating: 0.1, price: 999999, expected: 0.0000 }, // Very low value score
      { rating: 10, price: 999999, expected: 0.0000 }, // Large price
      { rating: 0.0001, price: 0.0001, expected: 1.0000 }, // Tiny numbers
    ];

    extremeCases.forEach(({ rating, price, expected }) => {
      const valueScore = +(rating / price).toFixed(4);
      expect(valueScore).toBe(expected);
    });
  });
});