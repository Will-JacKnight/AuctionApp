# Use a lightweight Node.js image
FROM node:18-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the app's source code
COPY . .

# Create env.js at build time
## RUN echo "window.API_URL = '${API_GATEWAY_HEROKU_URL}';" > /app/public/env.js

# Expose the Vite development server port
EXPOSE 5173

# Start Vite dev server
CMD ["sh", "-c", "npm audit fix && npm run dev -- --host"]
