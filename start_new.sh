#!/bin/bash

# StudySync V2 Startup Script
echo "🚀 Starting StudySync V2 - UNC Class Rating System"

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "📦 Starting MongoDB..."
    if command -v docker &> /dev/null; then
        docker-compose up -d mongodb || {
            echo "⚠️  Failed to start MongoDB with Docker. Please ensure docker-compose.yml is configured correctly."
            echo "   Or start MongoDB manually: brew services start mongodb-community"
            exit 1
        }
    else
        echo "⚠️  Docker not found. Please start MongoDB manually: brew services start mongodb-community"
    fi
else
    echo "✅ MongoDB is already running"
fi

# Setup backend environment
echo "🔧 Setting up backend environment..."
cd /Users/juanperdomo/development/ScheduleMaker/backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📦 Installing/upgrading Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env file and set your JWT_SECRET_KEY"
fi

# Start backend server
echo "🚀 Starting FastAPI backend server..."
echo "Backend will be available at: http://localhost:8000"
echo "API documentation will be available at: http://localhost:8000/docs"

# Start the backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Setup and start frontend
echo "🔧 Setting up frontend environment..."
cd /Users/juanperdomo/development/ScheduleMaker/frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Start frontend server
echo "🚀 Starting React frontend server..."
echo "Frontend will be available at: http://localhost:5173"
npm run dev &
FRONTEND_PID=$!

# Function to cleanup processes on exit
cleanup() {
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

echo ""
echo "🎉 StudySync V2 is starting up!"
echo ""
echo "📱 Frontend: http://localhost:5173"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID