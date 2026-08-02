# Use official lightweight Node.js Alpine base image
FROM node:18-alpine

# Set working directory inside container
WORKDIR /app

# Copy package definition files
COPY package*.json ./

# Install production dependencies
RUN npm install --omit=dev

# Copy application files
COPY . .

# Set default environment variables
ENV PORT=3000
ENV FLAG1="AEGIS{ENTRY-7D9A-88E2}"
ENV FLAG2="AEGIS{PRIV-C4F8-15B7}"
ENV FLAG3="AEGIS{CHMR-E1A6-9D40}"

# Expose server port
EXPOSE 3000

# Start CTF server
CMD ["node", "server.js"]
