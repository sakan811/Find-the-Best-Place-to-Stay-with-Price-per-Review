import Link from 'next/link';

export default function Home() {

  return (
    <div className="space-y-10">
      {/* Hero Section */}
      <section className="relative bg-blue-600 text-white rounded-lg overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-blue-800 opacity-90 z-0"></div>
        <div className="relative z-10 px-8 py-16 md:py-24 max-w-5xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6 whitespace-nowrap px-4">
            Find the Best Value Hotels for Your Stay
          </h1>
          <p className="text-xl mb-8">
            Compare hotels based on review-per-price ratio to get the most value for your money
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/hotels/add"
              className="bg-white text-blue-600 px-6 py-3 rounded-lg font-medium hover:bg-gray-100 transition-colors"
            >
              Add a Hotel
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
