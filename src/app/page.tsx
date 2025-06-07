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

export default function Home() {
  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-pink-500 via-rose-400 to-pink-600 text-white rounded-3xl overflow-hidden shadow-2xl">
        {/* Decorative elements */}
        <div className="absolute inset-0 bg-gradient-to-r from-pink-500/90 to-rose-500/90 z-0"></div>
        <div className="absolute top-4 right-4 text-6xl opacity-20">🌸</div>
        <div className="absolute bottom-4 left-4 text-4xl opacity-15">🌸</div>
        <div className="absolute top-1/2 left-1/4 text-2xl opacity-10">🌸</div>

        <div className="relative z-10 px-8 py-20 md:py-28 max-w-5xl mx-auto text-center">
          <div className="mb-4">
            <span className="text-6xl">🌸</span>
          </div>
          <h1 className="text-4xl md:text-6xl font-bold mb-8 leading-tight">
            Find the Best Value Hotels
            <span className="block text-pink-100">with SakuYado</span>
          </h1>
          <p className="text-xl md:text-2xl mb-10 text-pink-50 max-w-3xl mx-auto leading-relaxed">
            Compare hotels based on review-per-price ratio to get the most value
            for your money
          </p>
          <div className="flex flex-col sm:flex-row gap-6 justify-center">
            <Link
              href="/hotels/add"
              className="bg-white text-pink-600 px-8 py-4 rounded-2xl font-bold text-lg hover:bg-pink-50 hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl"
            >
              🌸 Add a Hotel
            </Link>
            <Link
              href="/hotels/compare"
              className="bg-pink-600 text-white px-8 py-4 rounded-2xl font-bold text-lg hover:bg-pink-700 hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl border-2 border-pink-300"
            >
              Compare Hotels
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}