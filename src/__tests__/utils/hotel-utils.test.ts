import { describe, expect, it } from "vitest";

// Utility functions for testing (could be extracted to a separate file in a real app)
export const calculateValueScore = (rating: number, price: number): number => {
  return parseFloat((rating / price).toFixed(4));
};

export const sortHotelsByValueScore = (hotels: any[]): any[] => {
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
        { name: "Hotel A", valueScore: 0.05 },
        { name: "Hotel B", valueScore: 0.08 },
        { name: "Hotel C", valueScore: 0.06 },
      ];

      const sorted = sortHotelsByValueScore(hotels);

      expect(sorted[0].name).toBe("Hotel B");
      expect(sorted[1].name).toBe("Hotel C");
      expect(sorted[2].name).toBe("Hotel A");
    });

    it("should maintain original array order for equal value scores", () => {
      const hotels = [
        { name: "Hotel A", valueScore: 0.05 },
        { name: "Hotel B", valueScore: 0.05 },
        { name: "Hotel C", valueScore: 0.06 },
      ];

      const sorted = sortHotelsByValueScore(hotels);

      expect(sorted[0].name).toBe("Hotel C");
      expect(sorted[1].name).toBe("Hotel A");
      expect(sorted[2].name).toBe("Hotel B");
    });
  });
});
