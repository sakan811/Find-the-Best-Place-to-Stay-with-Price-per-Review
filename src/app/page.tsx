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

import Link from "next/link";

export default function ResponsiveHomePage() {
  return (
    <div className="space-y-8 sm:space-y-12">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-pink-500 via-rose-400 to-pink-600 text-white rounded-2xl sm:rounded-3xl overflow-hidden shadow-xl sm:shadow-2xl">
        {/* Decorative elements */}
        <div className="absolute inset-0 bg-gradient-to-r from-pink-500/90 to-rose-500/90 z-0"></div>
        <div className="absolute top-2 right-2 sm:top-4 sm:right-4 text-4xl sm:text-6xl opacity-20">
          🌸
        </div>
        <div className="absolute bottom-2 left-2 sm:bottom-4 sm:left-4 text-2xl sm:text-4xl opacity-15">
          🌸
        </div>
        <div className="absolute top-1/2 left-1/4 text-xl sm:text-2xl opacity-10 hidden sm:block">
          🌸
        </div>

        <div className="relative z-10 px-4 sm:px-8 py-12 sm:py-16 md:py-20 lg:py-28 max-w-5xl mx-auto text-center">
          <div className="mb-3 sm:mb-4">
            <span className="text-4xl sm:text-5xl md:text-6xl">🌸</span>
          </div>

          {/* Responsive title */}
          <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold mb-4 sm:mb-6 md:mb-8 leading-tight">
            Find the Best Value Hotels
            <span className="block text-pink-100 mt-1 sm:mt-2">
              with SakuYado
            </span>
          </h1>

          {/* Responsive description */}
          <p className="text-base sm:text-lg md:text-xl lg:text-2xl mb-6 sm:mb-8 md:mb-10 text-pink-50 max-w-3xl mx-auto leading-relaxed px-2 sm:px-0">
            Compare hotels based on review-per-price ratio to get the most value
            for your money
          </p>

          {/* Responsive buttons */}
          <div className="flex flex-col sm:flex-row gap-4 sm:gap-6 justify-center max-w-md sm:max-w-none mx-auto">
            <Link
              href="/hotels/add"
              className="w-full sm:w-auto bg-white text-pink-600 px-6 sm:px-8 py-3 sm:py-4 rounded-xl sm:rounded-2xl font-bold text-base sm:text-lg hover:bg-pink-50 hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl text-center"
            >
              🌸 Add a Hotel
            </Link>
            <Link
              href="/hotels/compare"
              className="w-full sm:w-auto bg-pink-600 text-white px-6 sm:px-8 py-3 sm:py-4 rounded-xl sm:rounded-2xl font-bold text-base sm:text-lg hover:bg-pink-700 hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl border-2 border-pink-300 text-center"
            >
              Compare Hotels
            </Link>
          </div>
        </div>
      </section>

      {/* How it works - responsive layout */}
      <section className="bg-gradient-to-br from-pink-50 to-white p-4 sm:p-6 md:p-8 rounded-2xl sm:rounded-3xl border-2 border-pink-200">
        <div className="text-center mb-6 sm:mb-8">
          <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold text-pink-800 mb-2 sm:mb-4">
            How SakuYado Works
          </h2>
          <p className="text-sm sm:text-base md:text-lg text-pink-600">
            Three simple steps to find your perfect hotel
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6 md:gap-8">
          <div className="text-center">
            <div className="w-12 h-12 sm:w-16 sm:h-16 bg-pink-500 text-white rounded-full flex items-center justify-center mx-auto mb-3 sm:mb-4 font-bold text-lg sm:text-xl">
              1
            </div>
            <h3 className="text-lg sm:text-xl font-bold text-pink-800 mb-2">
              Add Hotels
            </h3>
            <p className="text-sm sm:text-base text-pink-600">
              Input hotel names, prices, and ratings
            </p>
          </div>

          <div className="text-center">
            <div className="w-12 h-12 sm:w-16 sm:h-16 bg-rose-500 text-white rounded-full flex items-center justify-center mx-auto mb-3 sm:mb-4 font-bold text-lg sm:text-xl">
              2
            </div>
            <h3 className="text-lg sm:text-xl font-bold text-rose-800 mb-2">
              Auto Calculate
            </h3>
            <p className="text-sm sm:text-base text-rose-600">
              We calculate value scores automatically
            </p>
          </div>

          <div className="text-center">
            <div className="w-12 h-12 sm:w-16 sm:h-16 bg-pink-500 text-white rounded-full flex items-center justify-center mx-auto mb-3 sm:mb-4 font-bold text-lg sm:text-xl">
              3
            </div>
            <h3 className="text-lg sm:text-xl font-bold text-pink-800 mb-2">
              Compare & Choose
            </h3>
            <p className="text-sm sm:text-base text-pink-600">
              See ranked results and pick the best value
            </p>
          </div>
        </div>
      </section>

      {/* Decorative Elements - responsive */}
      <div className="text-center space-x-3 sm:space-x-6 opacity-60">
        <span className="text-2xl sm:text-3xl animate-pulse">🌸</span>
        <span className="text-3xl sm:text-4xl animate-pulse delay-1000">
          🌸
        </span>
        <span className="text-2xl sm:text-3xl animate-pulse delay-2000">
          🌸
        </span>
      </div>
    </div>
  );
}
