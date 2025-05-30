import { MetadataRoute } from 'next'

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'Hotel Value Analyzer',
    short_name: 'HotelValue',
    description: 'Compare hotels based on review-per-price ratio',
    start_url: '/',
    display: 'standalone',
    background_color: '#ffffff',
    theme_color: '#ec4899',
    icons: [
      {
        src: 'src/app/favicon.ico',
        sizes: 'any',
        type: 'image/x-icon',
      }
    ],
  }
}