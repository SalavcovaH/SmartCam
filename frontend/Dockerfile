# frontend/Dockerfile
FROM node:23

WORKDIR /app

# Install Node.js and npm
RUN apt-get update && apt-get install -y nodejs npm

COPY package.json package-lock.json ./
RUN npm install

COPY . .

CMD ["npm", "start"]