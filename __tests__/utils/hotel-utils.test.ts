import { describe, expect, it } from "vitest";

// Define the Hotel interface to match the application's Hotel type
interface Hotel {
  name: string;
  price: number;
  rating: number;
  currency?: string;
  valueScore: number;
}

// Utility functions for testing (could be extracted to a separate file in a real app)
export const calculateValueScore = (rating: number, price: number): number => {
  return parseFloat((rating / price).toFixed(4));
};

export const sortHotelsByValueScore = (hotels: Hotel[]): Hotel[] => {
  return [...hotels].sort((a, b) => b.valueScore - a.valueScore);
};

describe("Hotel Utility Functions", () => {
  describe("calculateValueScore", () => {
    it("should calculate value score correctly", () => {
      expect(calculateValueScore(8, 100)).toBe(0.08);
      expect(calculateValueScore(9, 150)).toBe(0.06);
      expect(calculateValueScore(10, 200)).toBe(0.05);
    });

    it("should handle decimal ratings", () => {
      expect(calculateValueScore(8.5, 100)).toBe(0.085);
      expect(calculateValueScore(9.2, 150)).toBe(0.0613);
    });
  });

  describe("sortHotelsByValueScore", () => {
    it("should sort hotels by value score in descending order", () => {
      const hotels = [
        { name: "Hotel A", price: 100, rating: 8, valueScore: 0.05 },
        { name: "Hotel B", price: 100, rating: 9, valueScore: 0.08 },
        { name: "Hotel C", price: 100, rating: 9, valueScore: 0.06 },
      ];

      const sorted = sortHotelsByValueScore(hotels);

      expect(sorted[0].name).toBe("Hotel B");
      expect(sorted[1].name).toBe("Hotel C");
      expect(sorted[2].name).toBe("Hotel A");
    });

    it("should maintain original array order for equal value scores", () => {
      const hotels = [
        { name: "Hotel A", price: 100, rating: 8, valueScore: 0.05 },
        { name: "Hotel B", price: 150, rating: 9, valueScore: 0.05 },
        { name: "Hotel C", price: 150, rating: 9, valueScore: 0.06 },
      ];

      const sorted = sortHotelsByValueScore(hotels);

      expect(sorted[0].name).toBe("Hotel C");
      expect(sorted[1].name).toBe("Hotel A");
      expect(sorted[2].name).toBe("Hotel B");
    });
  });
});
