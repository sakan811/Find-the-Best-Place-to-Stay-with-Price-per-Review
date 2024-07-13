# Use an official Node runtime as a parent image
FROM node:21

# Set the working directory in the container
WORKDIR /frontend

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code into the container
COPY . ./

# Build the React app for production
RUN npm run build

# Expose the port on which React runs (typically 3000)
EXPOSE 3000

# Run npm start
CMD ["npm", "start"]
