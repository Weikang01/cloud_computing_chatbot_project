# Stage 1: Build
FROM node:14 as build-stage

WORKDIR /app

ARG VITE_API_SERVER_URL
ENV VITE_API_SERVER_URL=$VITE_API_SERVER_URL

COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve
FROM nginx:stable-alpine as production-stage

# Copy the built assets from the build stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copy your custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the start script into the image
COPY start.sh /start.sh

# Make the start script executable
RUN chmod +x /start.sh

# Expose port 5173 to the outside
EXPOSE 5173

# Use the start script as the entrypoint
CMD ["/start.sh"]
