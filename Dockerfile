# Use official lightweight Python Alpine base image
FROM python:3.11-alpine

# Set working directory inside container
WORKDIR /app

# Copy application files
COPY . .

# Set environment variables
ENV PORT=3000
ENV PYTHONUNBUFFERED=1
ENV FLAG1="AEGIS{ENTRY-7D9A-88E2}"
ENV FLAG2="AEGIS{PRIV-C4F8-15B7}"
ENV FLAG3="AEGIS{CHMR-E1A6-9D40}"

# Expose server port
EXPOSE 3000

# Start Python CTF Server
CMD ["python3", "server.py"]
