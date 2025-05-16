'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';

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

  // Function to get currency symbol
  const getCurrencySymbol = (currency: string): string => {
    const symbols: {[key: string]: string} = {
      'USD': '$', 'EUR': '€', 'GBP': '£', 
      'JPY': '¥', 'CAD': 'C$', 'AUD': 'A$'
    };
    return symbols[currency] || '';
  };

  useEffect(() => {
    // Load hotels and calculate scores
    try {
      const savedHotels = localStorage.getItem('hotels');
      if (savedHotels) {
        const parsedHotels: Hotel[] = JSON.parse(savedHotels);
        
        // Calculate and sort by value score
        setHotels(parsedHotels
          .map(hotel => ({
            ...hotel,
            valueScore: parseFloat((hotel.rating / hotel.price).toFixed(4))
          }))
          .sort((a, b) => (b.valueScore || 0) - (a.valueScore || 0))
        );
      }
    } catch (error) {
      console.error('Error loading hotels:', error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  if (isLoading) {
    return <div className="text-center p-6">Loading hotel comparisons...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h1 className="text-2xl font-bold mb-6 text-center">Hotel Value Comparison</h1>
      
      {hotels.length === 0 ? (
        <div className="text-center my-8">
          <p className="mb-10">No hotels have been added yet.</p>
          <Link href="/hotels/add" className="bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700">
            Add Your First Hotel
          </Link>
        </div>
      ) : (
        <>
          <table className="min-w-full">
            <thead className="bg-gray-100">
              <tr>
                <th className="py-3 px-4 text-left">Rank</th>
                <th className="py-3 px-4 text-left">Hotel Name</th>
                <th className="py-3 px-4 text-left">Price</th>
                <th className="py-3 px-4 text-left">Rating (0-10)</th>
                <th className="py-3 px-4 text-left">Value Score</th>
              </tr>
            </thead>
            <tbody>
              {hotels.map((hotel, index) => (
                <tr key={index} className={index === 0 ? "bg-green-50" : index % 2 === 0 ? "bg-gray-50" : ""}>
                  <td className="py-2 px-4 border-b">{index + 1}</td>
                  <td className="py-2 px-4 border-b font-medium">
                    {hotel.name}
                    {index === 0 && <span className="ml-2 text-green-600 text-sm">(Best Value)</span>}
                  </td>
                  <td className="py-2 px-4 border-b">
                    {getCurrencySymbol(hotel.currency)}{hotel.price.toFixed(2)} {hotel.currency}
                  </td>
                  <td className="py-2 px-4 border-b">{hotel.rating.toFixed(1)}</td>
                  <td className="py-2 px-4 border-b">
                    {hotel.valueScore?.toFixed(4)}
                    <span className="text-gray-500 text-sm ml-1">(Rating/Price)</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          
          <div className="mt-6 flex justify-between">
            <Link href="/hotels/add" className="bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700">
              Add Another Hotel
            </Link>
            <button 
              onClick={() => { localStorage.removeItem('hotels'); setHotels([]); }}
              className="bg-red-500 text-white py-2 px-4 rounded-md hover:bg-red-600"
            >
              Clear All Hotels
            </button>
          </div>
          
          <div className="mt-6 p-4 bg-gray-50 rounded-lg">
            <h2 className="text-lg font-semibold mb-1">How We Calculate Value</h2>
            <p>The value score is the ratio of rating to price (Rating/Price). Higher scores indicate better value.</p>
          </div>
        </>
      )}
    </div>
  );
}