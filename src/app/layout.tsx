import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "Hotel Value Analyzer",
  description:
    "Compare hotels based on review-per-price ratio to get the most value for your money",
  keywords: [
    "hotel comparison",
    "travel deals",
    "value analyzer",
    "accommodation",
    "hotel reviews",
  ],
  openGraph: {
    title: "Hotel Value Analyzer",
    description:
      "Compare hotels based on review-per-price ratio to get the most value for your money",
    url: "https://hotel-value-analyzer.vercel.app",
    siteName: "Hotel Value Analyzer",
    images: [
      {
        url: "src/app/favicon.ico",
      },
    ],
    locale: "en_US",
    type: "website",
  },
};

const organizationStructuredData = {
  "@context": "https://schema.org",
  "@type": "WebApplication",
  name: "Hotel Value Analyzer",
  description:
    "Compare hotels based on review-per-price ratio to get the most value for your money",
  url: "https://hotel-value-analyzer.vercel.app",
  applicationCategory: "TravelApplication",
  operatingSystem: "Any",
  browserRequirements: "Requires JavaScript",
  offers: {
    "@type": "Offer",
    price: "0",
    priceCurrency: "USD",
  },
  featureList: [
    "Hotel price comparison",
    "Value score calculation",
    "Multi-currency support",
    "Rating analysis",
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gradient-to-br from-pink-50 via-white to-rose-100">
        {/* Structured Data */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify(organizationStructuredData),
          }}
        />

        {/* Decorative sakura petals background */}
        <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
          <div className="absolute top-10 left-10 w-4 h-4 bg-pink-300 rounded-full opacity-20 animate-pulse"></div>
          <div className="absolute top-32 right-20 w-3 h-3 bg-rose-300 rounded-full opacity-30 animate-pulse delay-1000"></div>
          <div className="absolute top-64 left-1/4 w-2 h-2 bg-pink-400 rounded-full opacity-25 animate-pulse delay-2000"></div>
          <div className="absolute bottom-32 right-1/3 w-3 h-3 bg-rose-200 rounded-full opacity-20 animate-pulse delay-3000"></div>
          <div className="absolute bottom-64 left-1/2 w-4 h-4 bg-pink-200 rounded-full opacity-15 animate-pulse delay-4000"></div>
        </div>

        <header className="relative z-10 bg-gradient-to-r from-pink-500 via-rose-400 to-pink-600 shadow-lg border-b-4 border-pink-200">
          <div className="container mx-auto px-4 py-6 flex justify-between items-center">
            <Link
              href="/"
              className="text-2xl font-bold text-white hover:text-pink-100 transition-colors duration-300 drop-shadow-sm"
            >
              🌸 Hotel Value Analyzer
            </Link>
          </div>
        </header>

        <main className="relative z-10 container mx-auto px-4 py-8">
          {children}
        </main>
      </body>
    </html>
  );
}
