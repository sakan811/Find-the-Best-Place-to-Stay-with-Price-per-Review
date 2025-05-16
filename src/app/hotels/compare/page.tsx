'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';

interface Hotel {
  name: string;
  price: number;
  rating: number;
  valueScore?: number;
}

export default function CompareHotelsPage() {
  const [hotels, setHotels] = useState<Hotel[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Get hotels from localStorage
    const loadHotels = () => {
      try {
        const savedHotels = localStorage.getItem('hotels');
        if (savedHotels) {
          // Calculate value score (rating/price ratio) for each hotel
          const parsedHotels: Hotel[] = JSON.parse(savedHotels);
          const hotelsWithScore = parsedHotels.map(hotel => ({
            ...hotel,
            valueScore: parseFloat((hotel.rating / hotel.price).toFixed(4))
          }));
          
          // Sort by best value (highest rating/price ratio)
          hotelsWithScore.sort((a, b) => (b.valueScore || 0) - (a.valueScore || 0));
          
          setHotels(hotelsWithScore);
        }
      } catch (error) {
        console.error('Error loading hotels:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadHotels();
  }, []);

  const clearAllHotels = () => {
    localStorage.removeItem('hotels');
    setHotels([]);
  };

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg text-center">
        <p>Loading hotel comparisons...</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg">
      <h1 className="text-2xl font-bold mb-6 text-center">Hotel Value Comparison</h1>
      
      {hotels.length === 0 ? (
        <div className="text-center my-10">
          <p className="mb-4">No hotels have been added yet.</p>
          <Link 
            href="/hotels/add" 
            className="bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700"
          >
            Add Your First Hotel
          </Link>
        </div>
      ) : (
        <>
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white">
              <thead className="bg-gray-100">
                <tr>
                  <th className="py-3 px-4 text-left">Rank</th>
                  <th className="py-3 px-4 text-left">Hotel Name</th>
                  <th className="py-3 px-4 text-left">Price ($)</th>
                  <th className="py-3 px-4 text-left">Rating</th>
                  <th className="py-3 px-4 text-left">Value Score</th>
                </tr>
              </thead>
              <tbody>
                {hotels.map((hotel, index) => (
                  <tr 
                    key={index} 
                    className={index === 0 ? "bg-green-50" : index % 2 === 0 ? "bg-gray-50" : ""}
                  >
                    <td className="py-3 px-4 border-b">{index + 1}</td>
                    <td className="py-3 px-4 border-b font-medium">
                      {hotel.name}
                      {index === 0 && <span className="ml-2 text-green-600 text-sm">(Best Value)</span>}
                    </td>
                    <td className="py-3 px-4 border-b">${hotel.price.toFixed(2)}</td>
                    <td className="py-3 px-4 border-b">{hotel.rating.toFixed(1)}</td>
                    <td className="py-3 px-4 border-b">
                      {hotel.valueScore?.toFixed(4)}
                      <span className="text-gray-500 text-sm ml-1">(Rating/Price)</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          <div className="mt-6 flex justify-between">
            <Link 
              href="/hotels/add" 
              className="bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700"
            >
              Add Another Hotel
            </Link>
            <button 
              onClick={clearAllHotels}
              className="bg-red-500 text-white py-2 px-4 rounded-md hover:bg-red-600"
            >
              Clear All Hotels
            </button>
          </div>
          
          <div className="mt-8 p-4 bg-gray-50 rounded-lg">
            <h2 className="text-lg font-semibold mb-2">How We Calculate Value</h2>
            <p>
              The value score is calculated as the ratio of hotel rating to price (Rating/Price).
              A higher value score indicates a better deal - more rating points per dollar spent.
            </p>
          </div>
        </>
      )}
    </div>
  );
}