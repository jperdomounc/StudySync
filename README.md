# StudySync

StudySync is a full-stack web application that helps college students generate optimized class schedules. Built with a React frontend and FastAPI backend, the platform streamlines the course selection process by allowing users to paste in their shopping cart and current schedule to receive conflict-free scheduling options.

## Project Overview

Many students struggle with building ideal class schedules, especially when balancing multiple course options and section times. StudySync simplifies this by:

- Parsing raw schedule information copied from a university portal
- Detecting time conflicts and fitting classes around existing commitments
- Suggesting optimized schedules based on availability, preferences, or course load

## Features

- Paste-in support for shopping cart and schedule data
- Backend logic to identify valid, conflict-free schedule combinations
- Ranked output based on fit and user-defined constraints (planned)
- Modular design for future expansion (e.g., professor ratings, preferred times)

## Tech Stack

- **Frontend:** React (Vite)
- **Backend:** FastAPI (Python)
- **Database:** MongoDB (for notes and schedule storage)
- **Environment Management:** Python venv, Node.js

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- Docker (for MongoDB)

### Database Setup (MongoDB)

1. **Start MongoDB using Docker:**
   ```bash
   # Make the setup script executable
   chmod +x setup-mongodb.sh
   
   # Run the setup script
   ./setup-mongodb.sh
   ```

2. **Alternative: Manual Docker setup:**
   ```bash
   docker-compose up -d mongodb
   ```

3. **Alternative: Local MongoDB installation:**
   ```bash
   # macOS with Homebrew
   brew install mongodb-community
   brew services start mongodb-community
   ```

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Set up virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn main:app --reload
