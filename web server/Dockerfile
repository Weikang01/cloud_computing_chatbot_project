# Stage 1: Build
# Use an official Node.js runtime as a parent image
FROM node:14 as build-stage

# Set the working directory in the container
WORKDIR /app

# Pass the API server URL as a build argument
ARG VITE_API_SERVER_URL

# Make the build argument available as an environment variable for Vite
ENV VITE_API_SERVER_URL=$VITE_API_SERVER_URL

# Copy package.json and package-lock.json (or yarn.lock) to the working directory
COPY package*.json ./
# If you're using yarn and have a yarn.lock file, you might want to copy it as well
# COPY yarn.lock ./

# Install project dependencies
RUN npm install
# If you're using yarn, use the following command instead
# RUN yarn install

# Copy the rest of your app's source code from your host to your image filesystem.
COPY . .

# Build the project for production
RUN npm run build
# If you're using yarn, use the following command instead
# RUN yarn build

# Stage 2: Serve
# Use an official lightweight Nginx image for serving the static files
FROM nginx:stable-alpine as production-stage

# Copy the built assets from the build stage to the default Nginx serve directory
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Expose port 80 to the outside once the container has launched
EXPOSE 80

# When the container starts, start Nginx server.
CMD ["nginx", "-g", "daemon off;"]
