"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

interface Hotel {
  name: string;
  price: number;
  rating: number;
  currency: string;
  valueScore?: number;
}

export default function CompareHotelsPage() {
  const [hotels, setHotels] = useState<Hotel[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    try {
      const savedHotels = JSON.parse(localStorage.getItem("hotels") || "[]");
      // Calculate value score and sort in one step
      const processedHotels = savedHotels
        .map((hotel: Hotel) => ({
          ...hotel,
          valueScore: +(hotel.rating / hotel.price).toFixed(4),
        }))
        .sort((a: Hotel, b: Hotel) => b.valueScore! - a.valueScore!);

      setHotels(processedHotels);
    } catch (error) {
      console.error("Error loading hotels:", error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  if (isLoading) {
    return (
      <div className="flex flex-col justify-center items-center h-64 space-y-4">
        <div className="text-6xl animate-pulse">🌸</div>
        <div className="text-xl text-pink-600 font-medium">
          Loading hotel comparisons...
        </div>
      </div>
    );
  }

  const hotelComparisonStructuredData = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    name: "Hotel Value Comparison",
    description: "Compare hotels by value score (rating/price ratio)",
    numberOfItems: hotels.length,
    itemListElement: hotels.map((hotel, index) => ({
      "@type": "ListItem",
      position: index + 1,
      item: {
        "@type": "LodgingBusiness",
        name: hotel.name,
        aggregateRating: {
          "@type": "AggregateRating",
          ratingValue: hotel.rating,
          bestRating: "10",
          worstRating: "1",
        },
        priceRange: `${hotel.price} ${hotel.currency}`,
        additionalProperty: {
          "@type": "PropertyValue",
          name: "Value Score",
          value: hotel.valueScore,
        },
      },
    })),
  };

  return (
    <div className="max-w-5xl mx-auto">
      {/* Structured Data Scripts */}
      {hotels.length > 0 && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify(hotelComparisonStructuredData),
          }}
        />
      )}

      {/* Header */}
      <div className="text-center mb-10">
        <div className="text-6xl mb-4">🏨</div>
        <h1 className="text-4xl font-bold text-pink-800 mb-4">
          Hotel Value Comparison
        </h1>
        <p className="text-pink-600 text-lg">
          Discover the best value accommodations
        </p>
      </div>

      {hotels.length === 0 ? (
        /* Empty State */
        <div className="text-center bg-gradient-to-br from-pink-50 via-white to-rose-50 p-12 rounded-3xl shadow-xl border-2 border-pink-200">
          <div className="text-8xl mb-6">🌸</div>
          <h2 className="text-2xl font-bold text-pink-800 mb-4">
            No Hotels Added Yet
          </h2>
          <p className="text-pink-600 mb-8 text-lg">
            Start your journey by adding your first hotel to compare
          </p>
          <Link
            href="/hotels/add"
            className="inline-block bg-gradient-to-r from-pink-500 to-rose-500 text-white py-4 px-8 rounded-2xl font-bold text-lg hover:from-pink-600 hover:to-rose-600 hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl"
          >
            🌸 Add Your First Hotel
          </Link>
        </div>
      ) : (
        <>
          {/* Table Container */}
          <div className="bg-gradient-to-br from-white via-pink-50 to-rose-50 rounded-3xl shadow-2xl border-2 border-pink-200 overflow-hidden mb-8">
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead className="bg-gradient-to-r from-pink-500 to-rose-500">
                  <tr>
                    <th className="py-4 px-6 text-left text-sm font-bold text-white uppercase tracking-wider">
                      🏆 Rank
                    </th>
                    <th className="py-4 px-6 text-left text-sm font-bold text-white uppercase tracking-wider">
                      🏨 Hotel
                    </th>
                    <th className="py-4 px-6 text-left text-sm font-bold text-white uppercase tracking-wider">
                      💰 Price
                    </th>
                    <th className="py-4 px-6 text-left text-sm font-bold text-white uppercase tracking-wider">
                      ⭐ Rating
                    </th>
                    <th className="py-4 px-6 text-left text-sm font-bold text-white uppercase tracking-wider">
                      🌸 Value Score
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {hotels.map((hotel, index) => (
                    <tr
                      key={index}
                      className={`
                        ${
                          index === 0
                            ? "bg-gradient-to-r from-pink-100 via-rose-100 to-pink-100 border-l-4 border-pink-400"
                            : index % 2 === 0
                              ? "bg-white/70"
                              : "bg-pink-50/50"
                        }
                        hover:bg-gradient-to-r hover:from-pink-100 hover:to-rose-100 transition-all duration-300
                        ${index !== hotels.length - 1 ? "border-b border-pink-200" : ""}
                      `}
                    >
                      <td className="py-4 px-6 whitespace-nowrap">
                        <div className="flex items-center space-x-2">
                          <span className="text-lg font-bold text-pink-700">
                            {index + 1}
                          </span>
                          {index === 0 && (
                            <span className="text-yellow-500 text-xl">👑</span>
                          )}
                        </div>
                      </td>
                      <td className="py-4 px-6 whitespace-nowrap">
                        <div className="font-bold text-pink-800 text-lg">
                          {hotel.name}
                          {index === 0 && (
                            <span className="ml-2 text-pink-500 text-sm font-normal">
                              🌸 Best Value
                            </span>
                          )}
                        </div>
                      </td>
                      <td className="py-4 px-6 whitespace-nowrap">
                        <span className="font-semibold text-pink-700 text-lg">
                          {hotel.price.toFixed(2)} {hotel.currency}
                        </span>
                      </td>
                      <td className="py-4 px-6 whitespace-nowrap">
                        <div className="flex items-center space-x-1">
                          <span className="font-semibold text-pink-700 text-lg">
                            {hotel.rating.toFixed(1)}
                          </span>
                          <span className="text-yellow-500">⭐</span>
                        </div>
                      </td>
                      <td className="py-4 px-6 whitespace-nowrap">
                        <span
                          className={`
                          font-bold text-lg px-3 py-1 rounded-full
                          ${
                            index === 0
                              ? "bg-gradient-to-r from-pink-200 to-rose-200 text-pink-800"
                              : "bg-pink-100 text-pink-700"
                          }
                        `}
                        >
                          {hotel.valueScore}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Value Score Explanation */}
          <div className="bg-gradient-to-r from-pink-100 via-white to-rose-100 p-6 rounded-2xl border-2 border-pink-200 shadow-lg mb-8">
            <div className="flex items-center space-x-3 mb-2">
              <span className="text-2xl">🧮</span>
              <h3 className="text-lg font-bold text-pink-800">
                Value Score Calculation
              </h3>
            </div>
            <p className="text-pink-700">
              <strong className="text-pink-800">Value Score</strong> = Rating ÷
              Price
              <span className="ml-2 text-sm">
                (higher score = better value for money)
              </span>
            </p>
          </div>

          {/* Action Buttons */}
          <div className="grid sm:grid-cols-2 gap-6">
            <Link
              href="/hotels/add"
              className="bg-gradient-to-r from-pink-500 to-rose-500 text-white py-4 px-6 rounded-2xl font-bold text-lg hover:from-pink-600 hover:to-rose-600 hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl text-center"
            >
              🌸 Add Another Hotel
            </Link>
            <button
              onClick={() => {
                localStorage.removeItem("hotels");
                setHotels([]);
              }}
              className="bg-gradient-to-r from-red-400 to-pink-400 text-white py-4 px-6 rounded-2xl font-bold text-lg hover:from-red-500 hover:to-pink-500 hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl"
            >
              🗑️ Clear All Hotels
            </button>
          </div>
        </>
      )}

      {/* Decorative Elements */}
      <div className="text-center mt-12 space-x-6">
        <span className="text-3xl opacity-60 animate-pulse">🌸</span>
        <span className="text-4xl opacity-80 animate-pulse delay-1000">🌸</span>
        <span className="text-3xl opacity-60 animate-pulse delay-2000">🌸</span>
      </div>
    </div>
  );
}
