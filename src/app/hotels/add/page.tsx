/*
 * SakuYado - A web application that helps you find the best value accommodations
 * Copyright (C) 2025  Sakan Nirattisaykul
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 * 
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function AddHotelPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    name: "",
    price: "",
    rating: "",
    currency: "USD",
  });
  const [errors, setErrors] = useState({
    name: "",
    price: "",
    rating: "",
    general: "", // Add general error for storage issues
  });

  // Load previously selected currency on component mount
  useEffect(() => {
    try {
      // Try to get the last used currency from localStorage
      const savedCurrency = localStorage.getItem("lastUsedCurrency");
      if (savedCurrency) {
        setFormData((prev) => ({
          ...prev,
          currency: savedCurrency,
        }));
      }
    } catch (error) {
      console.error("Error loading saved currency:", error);
      // Don't show error to user for loading preferences
    }
  }, []);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    // If currency is changed, save it to localStorage
    if (name === "currency") {
      try {
        localStorage.setItem("lastUsedCurrency", value);
      } catch (error) {
        console.error("Error saving currency preference:", error);
        // Don't show error for preference saving
      }
    }

    // Clear errors when user starts typing
    if (errors[name as keyof typeof errors]) {
      setErrors((prev) => ({
        ...prev,
        [name]: "",
        general: "", // Clear general error too
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {
      name: "",
      price: "",
      rating: "",
      general: "",
    };
    let isValid = true;

    if (!formData.name.trim()) {
      newErrors.name = "Hotel name is required";
      isValid = false;
    }

    const price = parseFloat(formData.price);
    if (isNaN(price) || price <= 0) {
      newErrors.price = "Price must be a positive number";
      isValid = false;
    }

    const rating = parseFloat(formData.rating);
    if (isNaN(rating) || rating < 0 || rating > 10) {
      newErrors.rating = "Rating must be between 0 and 10";
      isValid = false;
    }

    setErrors(newErrors);
    return isValid;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (validateForm()) {
      try {
        // Get existing hotels from local storage or initialize empty array
        const existingHotels = JSON.parse(localStorage.getItem("hotels") || "[]");

        // Add new hotel to the array
        const newHotel = {
          name: formData.name,
          price: parseFloat(formData.price),
          rating: parseFloat(formData.rating),
          currency: formData.currency,
        };

        const updatedHotels = [...existingHotels, newHotel];

        // Save to local storage - this might throw an error
        localStorage.setItem("hotels", JSON.stringify(updatedHotels));

        // Save the currency for future use
        localStorage.setItem("lastUsedCurrency", formData.currency);

        // Navigate to results page
        router.push("/hotels/compare");
      } catch (error) {
        console.error("Error saving hotel data:", error);
        
        // Set user-friendly error message
        setErrors((prev) => ({
          ...prev,
          general: "Unable to save hotel data. Please try again or check your browser storage settings.",
        }));
      }
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-white to-rose-100 px-4 py-4 sm:py-8">
      {/* Container with responsive max-width */}
      <div className="max-w-sm sm:max-w-md lg:max-w-lg xl:max-w-xl mx-auto">
        
        {/* Header Card - responsive spacing */}
        <div className="text-center mb-6 sm:mb-8">
          <div className="text-4xl sm:text-5xl md:text-6xl mb-3 sm:mb-4">🌸</div>
          <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-pink-800 mb-2">
            Add Hotel Information
          </h1>
          <p className="text-sm sm:text-base md:text-lg text-pink-600">
            Share your hotel details to find the best value
          </p>
        </div>

        {/* Form Card - enhanced responsive design */}
        <div className="bg-gradient-to-br from-white via-pink-50 to-rose-50 p-4 sm:p-6 md:p-8 rounded-2xl sm:rounded-3xl shadow-xl sm:shadow-2xl border-2 border-pink-200">
          <form onSubmit={handleSubmit} className="space-y-4 sm:space-y-6">
            
            {/* General Error Message */}
            {errors.general && (
              <div className="bg-red-50 border-2 border-red-200 rounded-xl p-3 sm:p-4">
                <p className="text-sm sm:text-base text-red-700 font-medium">
                  {errors.general}
                </p>
              </div>
            )}
            
            {/* Hotel Name - responsive input */}
            <div>
              <label
                htmlFor="name"
                className="block text-sm sm:text-base font-bold text-pink-800 mb-2"
              >
                🏨 Hotel Name
              </label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                className="w-full px-3 sm:px-4 py-2 sm:py-3 border-2 border-pink-200 rounded-xl sm:rounded-2xl focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400 bg-white/80 backdrop-blur transition-all duration-300 text-sm sm:text-base"
                placeholder="Enter hotel name"
              />
              {errors.name && (
                <p className="mt-1 sm:mt-2 text-xs sm:text-sm text-red-500 font-medium">
                  {errors.name}
                </p>
              )}
            </div>

            {/* Price and Currency - enhanced responsive layout */}
            <div>
              <label
                htmlFor="price"
                className="block text-sm sm:text-base font-bold text-pink-800 mb-2"
              >
                💰 Price
              </label>
              
              {/* Mobile: stacked, Tablet+: side-by-side */}
              <div className="flex flex-col sm:flex-row gap-2 sm:gap-3">
                <div className="flex-1">
                  <input
                    type="number"
                    id="price"
                    name="price"
                    value={formData.price}
                    onChange={handleChange}
                    className="w-full px-3 sm:px-4 py-2 sm:py-3 border-2 border-pink-200 rounded-xl sm:rounded-2xl focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400 bg-white/80 backdrop-blur transition-all duration-300 text-sm sm:text-base"
                    placeholder="Enter price"
                    min="0"
                    step="0.01"
                  />
                </div>
                
                {/* Currency dropdown - responsive width */}
                <div className="w-full sm:w-32 md:w-36 lg:w-40">
                  <select
                    id="currency"
                    name="currency"
                    value={formData.currency}
                    onChange={handleChange}
                    className="w-full px-2 sm:px-3 py-2 sm:py-3 border-2 border-pink-200 rounded-xl sm:rounded-2xl focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400 bg-white/80 backdrop-blur transition-all duration-300 text-xs sm:text-sm"
                  >
                    <option value="USD">USD</option>
                    <option value="EUR">EUR</option>
                    <option value="GBP">GBP</option>
                    {/* Add more currencies as needed */}
                  </select>
                </div>
              </div>
              
              {errors.price && (
                <p className="mt-1 sm:mt-2 text-xs sm:text-sm text-red-500 font-medium">
                  {errors.price}
                </p>
              )}
            </div>

            {/* Rating - responsive input */}
            <div>
              <label
                htmlFor="rating"
                className="block text-sm sm:text-base font-bold text-pink-800 mb-2"
              >
                ⭐ Rating (0-10)
              </label>
              <input
                type="number"
                id="rating"
                name="rating"
                value={formData.rating}
                onChange={handleChange}
                className="w-full px-3 sm:px-4 py-2 sm:py-3 border-2 border-pink-200 rounded-xl sm:rounded-2xl focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400 bg-white/80 backdrop-blur transition-all duration-300 text-sm sm:text-base"
                placeholder="Enter rating"
                min="0"
                max="10"
                step="0.1"
              />
              {errors.rating && (
                <p className="mt-1 sm:mt-2 text-xs sm:text-sm text-red-500 font-medium">
                  {errors.rating}
                </p>
              )}
            </div>

            {/* Submit Button - enhanced responsive */}
            <button
              type="submit"
              className="w-full bg-gradient-to-r from-pink-500 to-rose-500 text-white py-3 sm:py-4 px-4 sm:px-6 rounded-xl sm:rounded-2xl font-bold text-base sm:text-lg hover:from-pink-600 hover:to-rose-600 hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl"
            >
              🌸 Submit & Compare
            </button>

            {/* Secondary Actions - responsive layout */}
            <div className="space-y-3 sm:space-y-4">
              <Link
                href="/hotels/compare"
                className="block w-full bg-gradient-to-r from-white to-pink-50 text-pink-600 py-3 sm:py-4 px-4 sm:px-6 rounded-xl sm:rounded-2xl font-bold text-base sm:text-lg hover:from-pink-50 hover:to-rose-50 hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl text-center border-2 border-pink-200"
              >
                👀 View Compare Page
              </Link>
              
              <Link
                href="/"
                className="block w-full text-center text-sm sm:text-base text-pink-600 hover:text-pink-800 font-medium transition-colors duration-300"
              >
                ← Back to Home
              </Link>
            </div>
          </form>
        </div>

        {/* Decorative Elements - responsive */}
        <div className="text-center mt-6 sm:mt-8 space-x-2 sm:space-x-4">
          <span className="text-xl sm:text-2xl opacity-60">🌸</span>
          <span className="text-2xl sm:text-3xl opacity-80">🌸</span>
          <span className="text-xl sm:text-2xl opacity-60">🌸</span>
        </div>
      </div>
    </div>
  );
}