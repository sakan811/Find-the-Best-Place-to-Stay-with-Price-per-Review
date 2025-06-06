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
  });

  const addHotelPageSchema = {
    "@context": "https://schema.org",
    "@type": "WebPage",
    name: "Add Hotel Information - SakuYado",
    description:
      "Add hotel details to compare value and find the best accommodation deals with SakuYado",
    url: "https://saku-yado.vercel.app/hotels/add",
    isPartOf: {
      "@type": "WebSite",
      name: "SakuYado",
      url: "https://saku-yado.vercel.app",
    },
    mainEntity: {
      "@type": "WebApplication",
      name: "SakuYado Hotel Information Form",
      description:
        "Input hotel name, price, rating and currency for value comparison with SakuYado",
      applicationCategory: "TravelApplication",
      featureList: [
        "Hotel data input",
        "Multi-currency support",
        "Rating validation",
        "Value score calculation",
      ],
    },
    potentialAction: {
      "@type": "UseAction",
      target: "https://saku-yado.vercel.app/hotels/compare",
      name: "Compare Hotels with SakuYado",
    },
  };

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
      }
    }

    // Clear errors when user starts typing
    if (errors[name as keyof typeof errors]) {
      setErrors((prev) => ({
        ...prev,
        [name]: "",
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {
      name: "",
      price: "",
      rating: "",
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

      // Save to local storage
      localStorage.setItem("hotels", JSON.stringify(updatedHotels));

      // Save the currency for future use
      localStorage.setItem("lastUsedCurrency", formData.currency);

      // Navigate to results page
      router.push("/hotels/compare");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-8">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(addHotelPageSchema),
        }}
      />

      {/* Header Card */}
      <div className="text-center mb-8">
        <div className="text-6xl mb-4">🌸</div>
        <h1 className="text-3xl font-bold text-pink-800 mb-2">
          Add Hotel Information
        </h1>
        <p className="text-pink-600">
          Share your hotel details to find the best value
        </p>
      </div>

      {/* Form Card */}
      <div className="bg-gradient-to-br from-white via-pink-50 to-rose-50 p-8 rounded-3xl shadow-2xl border-2 border-pink-200">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Hotel Name */}
          <div>
            <label
              htmlFor="name"
              className="block text-sm font-bold text-pink-800 mb-2"
            >
              🏨 Hotel Name
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className="w-full px-4 py-3 border-2 border-pink-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400 bg-white/80 backdrop-blur transition-all duration-300"
              placeholder="Enter hotel name"
            />
            {errors.name && (
              <p className="mt-2 text-sm text-red-500 font-medium">
                {errors.name}
              </p>
            )}
          </div>

          {/* Price and Currency */}
          <div>
            <label
              htmlFor="price"
              className="block text-sm font-bold text-pink-800 mb-2"
            >
              💰 Price
            </label>
            <div className="flex space-x-3">
              <input
                type="number"
                id="price"
                name="price"
                value={formData.price}
                onChange={handleChange}
                className="flex-1 px-4 py-3 border-2 border-pink-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400 bg-white/80 backdrop-blur transition-all duration-300"
                placeholder="Enter price"
                min="0"
                step="0.01"
              />
              <select
                id="currency"
                name="currency"
                value={formData.currency}
                onChange={handleChange}
                className="px-4 py-3 border-2 border-pink-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400 bg-white/80 backdrop-blur transition-all duration-300 min-w-24"
              >
                <option value="AED">AED - United Arab Emirates Dirham</option>
                <option value="ARS">ARS - Argentine Peso</option>
                <option value="AUD">AUD - Australian Dollar</option>
                <option value="AZN">AZN - Azerbaijani Manat</option>
                <option value="BHD">BHD - Bahraini Dinar</option>
                <option value="BGN">BGN - Bulgarian Lev</option>
                <option value="BRL">BRL - Brazilian Real</option>
                <option value="CAD">CAD - Canadian Dollar</option>
                <option value="CHF">CHF - Swiss Franc</option>
                <option value="CLP">CLP - Chilean Peso</option>
                <option value="CNY">CNY - Chinese Yuan</option>
                <option value="COP">COP - Colombian Peso</option>
                <option value="CZK">CZK - Czech Koruna</option>
                <option value="DKK">DKK - Danish Krone</option>
                <option value="EGP">EGP - Egyptian Pound</option>
                <option value="EUR">EUR - Euro</option>
                <option value="FJD">FJD - Fijian Dollar</option>
                <option value="GBP">GBP - Pound Sterling</option>
                <option value="GEL">GEL - Georgian Lari</option>
                <option value="HKD">HKD - Hong Kong Dollar</option>
                <option value="HUF">HUF - Hungarian Forint</option>
                <option value="IDR">IDR - Indonesian Rupiah</option>
                <option value="ILS">ILS - Israeli New Shekel</option>
                <option value="INR">INR - Indian Rupee</option>
                <option value="ISK">ISK - Icelandic Króna</option>
                <option value="JPY">JPY - Japanese Yen</option>
                <option value="JOD">JOD - Jordanian Dinar</option>
                <option value="KRW">KRW - South Korean Won</option>
                <option value="KWD">KWD - Kuwaiti Dinar</option>
                <option value="KZT">KZT - Kazakhstani Tenge</option>
                <option value="MDL">MDL - Moldovan Leu</option>
                <option value="MOP">MOP - Macanese Pataca</option>
                <option value="MXN">MXN - Mexican Peso</option>
                <option value="MYR">MYR - Malaysian Ringgit</option>
                <option value="NAD">NAD - Namibian Dollar</option>
                <option value="NOK">NOK - Norwegian Krone</option>
                <option value="NZD">NZD - New Zealand Dollar</option>
                <option value="OMR">OMR - Omani Rial</option>
                <option value="PLN">PLN - Polish Złoty</option>
                <option value="QAR">QAR - Qatari Riyal</option>
                <option value="RON">RON - Romanian Leu</option>
                <option value="RUB">RUB - Russian Rouble</option>
                <option value="SAR">SAR - Saudi Arabian Riyal</option>
                <option value="SEK">SEK - Swedish Krona</option>
                <option value="SGD">SGD - Singapore Dollar</option>
                <option value="THB">THB - Thai Baht</option>
                <option value="TRY">TRY - Turkish Lira</option>
                <option value="TWD">TWD - New Taiwan Dollar</option>
                <option value="UAH">UAH - Ukrainian Hryvnia</option>
                <option value="USD">USD - United States Dollar</option>
                <option value="XOF">XOF - West African CFA Franc</option>
                <option value="ZAR">ZAR - South African Rand</option>
              </select>
            </div>
            {errors.price && (
              <p className="mt-2 text-sm text-red-500 font-medium">
                {errors.price}
              </p>
            )}
          </div>

          {/* Rating */}
          <div>
            <label
              htmlFor="rating"
              className="block text-sm font-bold text-pink-800 mb-2"
            >
              ⭐ Rating (0-10)
            </label>
            <input
              type="number"
              id="rating"
              name="rating"
              value={formData.rating}
              onChange={handleChange}
              className="w-full px-4 py-3 border-2 border-pink-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400 bg-white/80 backdrop-blur transition-all duration-300"
              placeholder="Enter rating"
              min="0"
              max="10"
              step="0.1"
            />
            {errors.rating && (
              <p className="mt-2 text-sm text-red-500 font-medium">
                {errors.rating}
              </p>
            )}
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            className="w-full bg-gradient-to-r from-pink-500 to-rose-500 text-white py-4 px-6 rounded-2xl font-bold text-lg hover:from-pink-600 hover:to-rose-600 hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl"
          >
            🌸 Submit & Compare
          </button>

          {/* Compare Page Link */}
          <Link
            href="/hotels/compare"
            className="block w-full bg-gradient-to-r from-white to-pink-50 text-pink-600 py-4 px-6 rounded-2xl font-bold text-lg hover:from-pink-50 hover:to-rose-50 hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl text-center border-2 border-pink-200"
          >
            View Compare Page
          </Link>
        </form>
      </div>

      {/* Decorative Elements */}
      <div className="text-center mt-8 space-x-4">
        <span className="text-2xl opacity-60">🌸</span>
        <span className="text-3xl opacity-80">🌸</span>
        <span className="text-2xl opacity-60">🌸</span>
      </div>
    </div>
  );
}