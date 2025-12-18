FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy project
COPY . .

# Build argument for API URL
ARG VITE_API_BASE_URL=http://localhost:8000
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

# Build
RUN npm run build

# Install serve to run the built app
RUN npm install -g serve

EXPOSE 3000

# Serve the built app
CMD ["serve", "-s", "dist", "-l", "3000"]
