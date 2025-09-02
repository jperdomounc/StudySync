#!/bin/bash

echo "Setting up MongoDB for ScheduleMaker..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Docker is not running. Please start Docker first."
    exit 1
fi

# Start MongoDB using Docker Compose
echo "Starting MongoDB container..."
docker-compose up -d mongodb

# Wait for MongoDB to be ready
echo "Waiting for MongoDB to be ready..."
sleep 10

# Test connection
echo "Testing MongoDB connection..."
docker exec schedulemaker-mongodb mongosh --eval "db.runCommand('ping')" > /dev/null

if [ $? -eq 0 ]; then
    echo "✅ MongoDB is running successfully!"
    echo "MongoDB is available at: mongodb://localhost:27017"
    echo "To stop MongoDB: docker-compose down"
else
    echo "❌ Failed to connect to MongoDB"
    exit 1
fi