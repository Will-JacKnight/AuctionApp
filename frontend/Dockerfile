# Step 1: Use an official Node.js runtime as a parent image
FROM node:18 AS build

# Set the working directory in the container
WORKDIR /app

# Step 3: Copy the package.json and package-lock.json
COPY package*.json ./

# Step 4: Install the dependencies
RUN npm install

# Step 5: Copy the rest of the application files
COPY . .

# Step 6: Build the React app for production
RUN npm run build

# Step 7: Use a lighter image to serve the React app
FROM nginx:alpine

# Step 8: Copy the build folder to the nginx server directory
COPY --from=build /app/dist /usr/share/nginx/html

# Step 9: Expose the default port for nginx
EXPOSE 80

# Step 10: Run nginx
CMD ["nginx", "-g", "daemon off;"]