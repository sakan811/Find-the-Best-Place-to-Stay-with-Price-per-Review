'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function AddHotelPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    name: '',
    price: '',
    rating: ''
  });
  const [errors, setErrors] = useState({
    name: '',
    price: '',
    rating: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear errors when user starts typing
    if (errors[name as keyof typeof errors]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {
      name: '',
      price: '',
      rating: ''
    };
    let isValid = true;

    if (!formData.name.trim()) {
      newErrors.name = 'Hotel name is required';
      isValid = false;
    }

    const price = parseFloat(formData.price);
    if (isNaN(price) || price <= 0) {
      newErrors.price = 'Price must be a positive number';
      isValid = false;
    }

    const rating = parseFloat(formData.rating);
    if (isNaN(rating) || rating < 0 || rating > 5) {
      newErrors.rating = 'Rating must be between 0 and 5';
      isValid = false;
    }

    setErrors(newErrors);
    return isValid;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (validateForm()) {
      // Get existing hotels from local storage or initialize empty array
      const existingHotels = JSON.parse(localStorage.getItem('hotels') || '[]');
      
      // Add new hotel to the array
      const newHotel = {
        name: formData.name,
        price: parseFloat(formData.price),
        rating: parseFloat(formData.rating)
      };
      
      const updatedHotels = [...existingHotels, newHotel];
      
      // Save to local storage
      localStorage.setItem('hotels', JSON.stringify(updatedHotels));
      
      // Navigate to results page
      router.push('/hotels/compare');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg">
      <h1 className="text-2xl font-bold mb-6 text-center">Add Hotel Information</h1>
      
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
            Hotel Name
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter hotel name"
          />
          {errors.name && <p className="mt-1 text-sm text-red-600">{errors.name}</p>}
        </div>
        
        <div className="mb-4">
          <label htmlFor="price" className="block text-sm font-medium text-gray-700 mb-1">
            Price per Night ($)
          </label>
          <input
            type="number"
            id="price"
            name="price"
            value={formData.price}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter price"
            min="0"
            step="0.01"
          />
          {errors.price && <p className="mt-1 text-sm text-red-600">{errors.price}</p>}
        </div>
        
        <div className="mb-6">
          <label htmlFor="rating" className="block text-sm font-medium text-gray-700 mb-1">
            Rating (0-5)
          </label>
          <input
            type="number"
            id="rating"
            name="rating"
            value={formData.rating}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter rating"
            min="0"
            max="5"
            step="0.1"
          />
          {errors.rating && <p className="mt-1 text-sm text-red-600">{errors.rating}</p>}
        </div>
        
        <div className="flex justify-between">
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Submit & Compare
          </button>
        </div>
      </form>
    </div>
  );
}