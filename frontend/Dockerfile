# Step 1: Build the React app
FROM node:22-alpine3.21 AS build

# Set the working directory and ensure it's owned by the non-root user
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React application
RUN npx vite build

# Step 2: Serve the React app with Nginx
FROM nginx:1.27.4-alpine3.21-slim

# Copy the build output to Nginx's html directory
COPY --from=build /app/dist /usr/share/nginx/html

# Copy a custom Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80 (Nginx default port)
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
