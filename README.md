# SakuYado 🌸

A beautiful web application that helps you find the best value accommodations by calculating a **Review/Price Score** for each hotel you input.

## What it does

- Add hotel information (name, price, rating, currency)
- Automatically calculates value scores (Rating ÷ Price)
- Ranks hotels by best value
- Compare multiple hotels side-by-side

Higher scores = better value for money! 🌸

## Status

[![Docker CI](https://github.com/sakan811/SakuYado/actions/workflows/docker-ci.yml/badge.svg)](https://github.com/sakan811/SakuYado/actions/workflows/docker-ci.yml)

[![Web App Test](https://github.com/sakan811/SakuYado/actions/workflows/web-app-test.yml/badge.svg)](https://github.com/sakan811/SakuYado/actions/workflows/web-app-test.yml)

## How to Use

### 🌐 Vercel (Recommended)

Simply visit: **<https://saku-yado.vercel.app/>**

### 🐳 Docker

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Clone this repository:

   ```bash
   git clone https://github.com/sakan811/SakuYado.git
   cd SakuYado
   ```

3. Run with Docker Compose:

   ```bash
   docker compose --profile pull up -d
   ```

4. Open <http://localhost:3000>

### 💻 Local Development

1. Setup [pnpm](https://pnpm.io/installation)

2. Clone the repository:

   ```bash
   git clone https://github.com/sakan811/SakuYado.git
   cd SakuYado
   ```

3. Install dependencies:

   ```bash
   pnpm install
   ```

4. Run the development server:

   ```bash
   pnpm run dev
   ```

5. Open <http://localhost:3000>
