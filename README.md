# Hotel Value Analyzer

A web application that helps you find the best value accommodations by calculating a **Review/Price Score** for each hotel you input.

## What it does

- Add hotel information (name, price, rating, currency)
- Automatically calculates value scores (Rating ÷ Price)
- Ranks hotels by best value
- Compare multiple hotels side-by-side

Higher scores = better value for money! 🌸

## Status

[![Docker CI](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/docker-ci.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/docker-ci.yml)

[![Web App Test](https://github.com/sakan811/hotel-value-analyzer/actions/workflows/web-app-test.yml/badge.svg)](https://github.com/sakan811/hotel-value-analyzer/actions/workflows/web-app-test.yml)

## How to Use

### 🌐 Vercel (Recommended)

Simply visit: **<https://hotel-value-analyzer.vercel.app/>**

### 🐳 Docker

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Clone this repository:

   ```bash
   git clone https://github.com/sakan811/hotel-value-analyzer.git
   cd hotel-value-analyzer
   ```

3. Run with Docker Compose:

   ```bash
   docker compose --profile pull up -d
   ```

4. Open <http://localhost:3000>

### 💻 Local Development

1. Clone the repository:

   ```bash
   git clone https://github.com/sakan811/hotel-value-analyzer.git
   cd hotel-value-analyzer
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Run the development server:

   ```bash
   npm run dev
   ```

4. Open <http://localhost:3000>
