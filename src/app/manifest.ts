import { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "SakuYado - Hotel Value Analyzer",
    short_name: "SakuYado",
    description: "Compare hotels based on review-per-price ratio with SakuYado",
    start_url: "/",
    display: "standalone",
    background_color: "#ffffff",
    theme_color: "#ec4899",
    icons: [
      {
        src: "src/app/favicon.ico",
        sizes: "any",
        type: "image/x-icon",
      },
    ],
  };
}