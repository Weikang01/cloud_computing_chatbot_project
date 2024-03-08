# Use an official Node.js base image
FROM node:14

# Set the working directory inside the container
WORKDIR /usr/src/app

# Pass the API server URL as a build argument
ARG INFERENCE_SERVER_URL

# Make the build argument available as an environment variable for Vite
ENV INFERENCE_SERVER_URL=$INFERENCE_SERVER_URL


# Copy package.json and package-lock.json (if available) to the working directory
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the rest of your application's source code to the working directory
COPY . .

# Expose the port your app runs on
EXPOSE 8000

# Define the command to run your app using npm start
CMD ["npm", "start"]
