## Use a lightweight Node.js image
#FROM node:18-alpine
#
## Set the working directory
#WORKDIR /app
#
## Copy package.json and install dependencies
#COPY package.json package-lock.json ./
#RUN npm install
#
## Copy the rest of the app's source code
#COPY . .
#
## Expose the Vite development server port
#EXPOSE 5173
#
## Start Vite dev server
#CMD ["npm", "run", "dev", "--", "--host"]

# Use a lightweight Node.js image
FROM node:18 AS build

# Set the working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the app's source code
COPY . .

# Build the React app for production
RUN npm run build

# Use a lightweight server to serve the static files
FROM node:18-alpine

# Install serve globally
RUN npm install -g serve

# Set the working directory
WORKDIR /app

# Copy the build files from the previous stage
COPY --from=build /app/dist ./build

# Expose the port the app runs on
EXPOSE 80

# Command to run the server
CMD ["serve", "-s", "build", "-l", "80"]