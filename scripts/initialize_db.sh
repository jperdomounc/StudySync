#!/bin/bash

# StudySync Database Initialization Script
# Populates the database with UNC course data for testing

echo "🗄️  StudySync Database Initialization"
echo "===================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "backend/initialize_data.py" ]; then
    echo -e "${YELLOW}[WARNING]${NC} Please run this script from the StudySync root directory"
    exit 1
fi

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo -e "${YELLOW}[WARNING]${NC} MongoDB doesn't appear to be running"
    echo "Please start MongoDB first:"
    echo "  - Using Docker: docker-compose up -d mongodb"
    echo "  - Using Homebrew: brew services start mongodb-community"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo -e "${GREEN}[INFO]${NC} Navigating to backend directory..."
cd backend

echo -e "${GREEN}[INFO]${NC} Activating virtual environment..."
if [ ! -f "venv/bin/activate" ]; then
    echo -e "${YELLOW}[WARNING]${NC} Virtual environment not found. Creating it..."
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo -e "${GREEN}[INFO]${NC} Running database initialization..."
python initialize_data.py

echo ""
echo -e "${GREEN}🎉 Database initialization complete!${NC}"
echo ""
echo "Your StudySync database is now populated with:"
echo "  • 8 UNC academic majors"
echo "  • 288+ real UNC courses"
echo "  • 580+ class difficulty ratings"
echo "  • 1,280+ professor reviews"
echo "  • 40 sample professors"
echo ""
echo "You can now:"
echo "  1. Start the backend: uvicorn main:app --reload"
echo "  2. Start the frontend: cd ../frontend && npm run dev"
echo "  3. Test with real UNC course data!"