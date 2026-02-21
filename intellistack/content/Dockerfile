# Docusaurus Content Site Dockerfile
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --production=false

# Copy source
COPY . .

# Build static site
RUN npm run build

# Install serve for static hosting
RUN npm install -g serve

# Expose port
EXPOSE 3000

# Serve the built site (serve uses PORT env var automatically)
CMD ["npx", "serve", "build", "-s"]
