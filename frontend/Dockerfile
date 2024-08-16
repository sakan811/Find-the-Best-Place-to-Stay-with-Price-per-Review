# Step 1: Build the React app
FROM node:20-alpine AS build

# Create a non-root user and group
RUN addgroup -g 1010 appgroup && adduser -u 1010 -G appgroup -S appuser

# Set the working directory and ensure it's owned by the non-root user
WORKDIR /app
RUN chown appuser:appgroup /app

# Switch to the non-root user for the rest of the build stage
USER appuser

# Copy package.json and package-lock.json
COPY --chown=appuser:appgroup package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY --chown=appuser:appgroup . .

# Build the React application
RUN npx vite build

# Step 2: Serve the React app with Nginx
FROM nginx:alpine

# Create a non-root user and group for Nginx
RUN addgroup -g 1001 nginxgroup && adduser -u 1001 -S nginxuser -G nginxgroup

# Create and set ownership of Nginx directories to nginxuser
RUN mkdir -p /var/cache/nginx /var/run/nginx /var/log/nginx /etc/nginx/conf.d && \
    chown -R nginxuser:nginxgroup /var/cache/nginx /var/run/nginx /var/log/nginx /etc/nginx/conf.d /usr/share/nginx/html

# Copy the build output to Nginx's html directory, with proper ownership
COPY --from=build /app/dist /usr/share/nginx/html
RUN chown -R nginxuser:nginxgroup /usr/share/nginx/html

# Copy a custom Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf
RUN chown -R nginxuser:nginxgroup /etc/nginx/nginx.conf

# Expose port 80 (Nginx default port)
EXPOSE 80

# Switch to non-root user
USER nginxuser

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
