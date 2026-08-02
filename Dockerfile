# Use official lightweight Python Alpine base image
FROM python:3.11-alpine

# Set working directory inside container
WORKDIR /app

# Copy application files
COPY . .

# Install cryptography dependency for evidence generator
RUN pip install --no-cache-dir cryptography

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLAG1="AEGIS{ENTRY-7D9A-88E34}"
ENV FLAG2="AEGIS{PRIV-C4F8-15B7}"
ENV FLAG3="AEGIS{CHMR-E1A6-9D40}"

# Expose potential Railway ports
EXPOSE 3000
EXPOSE 8080
EXPOSE 80

# Start Python CTF Server
CMD ["python3", "server.py"]
