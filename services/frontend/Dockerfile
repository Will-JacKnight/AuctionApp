# Use a lightweight Node.js image
FROM node:18-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the app's source code
COPY . .

# Expose the Vite development server port
EXPOSE 5173

# Start Vite dev server
CMD ["npm", "run", "dev", "--", "--host"]