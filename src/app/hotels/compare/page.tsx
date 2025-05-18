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
      <div className="flex justify-center items-center h-64">
        Loading hotel comparisons...
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg">
      <h1 className="text-2xl font-bold mb-6 text-center">
        Hotel Value Comparison
      </h1>

      {hotels.length === 0 ? (
        <div className="text-center my-8">
          <p className="mb-6">No hotels have been added yet.</p>
          <Link
            href="/hotels/add"
            className="bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Add Your First Hotel
          </Link>
        </div>
      ) : (
        <>
          <div className="overflow-x-auto mb-6">
            <table className="min-w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Rank
                  </th>
                  <th className="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Hotel
                  </th>
                  <th className="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Price
                  </th>
                  <th className="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Rating
                  </th>
                  <th className="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Value
                  </th>
                </tr>
              </thead>
              <tbody>
                {hotels.map((hotel, index) => (
                  <tr
                    key={index}
                    className={
                      index === 0 ? "bg-green-50" : "border-t border-gray-200"
                    }
                  >
                    <td className="py-2 px-3 whitespace-nowrap">{index + 1}</td>
                    <td className="py-2 px-3 whitespace-nowrap font-medium">
                      {hotel.name}
                      {index === 0 && (
                        <span className="ml-1 text-green-600 text-xs">★</span>
                      )}
                    </td>
                    <td className="py-2 px-3 whitespace-nowrap">
                      {hotel.price.toFixed(2)} {hotel.currency}
                    </td>
                    <td className="py-2 px-3 whitespace-nowrap">
                      {hotel.rating.toFixed(1)}
                    </td>
                    <td className="py-2 px-3 whitespace-nowrap">
                      {hotel.valueScore}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="mb-6 p-3 bg-gray-50 rounded-md text-sm">
            <p>
              <strong>Value Score</strong> = Rating ÷ Price (higher is better
              value)
            </p>
          </div>

          <div className="flex justify-between space-x-4">
            <Link
              href="/hotels/add"
              className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 text-center"
            >
              Add Another Hotel
            </Link>
            <button
              onClick={() => {
                localStorage.removeItem("hotels");
                setHotels([]);
              }}
              className="flex-1 bg-red-500 text-white py-2 px-4 rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500"
            >
              Clear All Hotels
            </button>
          </div>
        </>
      )}
    </div>
  );
}
