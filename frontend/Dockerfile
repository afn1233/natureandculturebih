# Dockerfile for the React frontend
FROM node:20-slim

# Set working directory
WORKDIR /app

# Copy package files first (better caching)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy all frontend files
COPY . .

# Expose port 5173
EXPOSE 5173

# Start Vite dev server
CMD ["npm", "run", "dev"]