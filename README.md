# StudySync
**UNC Class & Professor Rating System**

StudySync is a full-stack web application designed exclusively for UNC students to rate class difficulty and professors. Built with secure UNC email authentication, the platform helps students make informed course selection decisions by providing community-driven ratings and reviews.

## Features

### 🔐 **Authentication System**
- UNC email validation (@unc.edu, @live.unc.edu, @ad.unc.edu)
- Secure password authentication with bcrypt hashing
- JWT token-based sessions
- User profiles displayed as "Major YYYY" format

### 📊 **Class Rating System**
- Rate class difficulty on a 1-10 scale
- View class rankings sorted by average difficulty
- Search functionality for finding specific classes
- Major-specific data filtering

### 👨‍🏫 **Professor Rating System** 
- Rate professors on a 1-5 star scale
- Write detailed reviews and experiences
- View professor ratings by class
- Professor statistics and rating counts

### 🎓 **Major-Based Organization**
- Browse ratings by academic major
- Only rate classes/professors within your major
- Major statistics and insights
- Comprehensive major list covering UNC programs

## Tech Stack

- **Frontend:** React + Vite
- **Backend:** FastAPI (Python)
- **Database:** MongoDB with indexed collections
- **Authentication:** JWT tokens with bcrypt password hashing
- **Styling:** Modern CSS with responsive design

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

# Create environment file (optional)
cp .env.example .env
# Edit .env with your JWT secret key

# Start the FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

### Quick Start

Use the provided script to start both services:

```bash
# Make script executable and run
chmod +x start_new.sh
./start_new.sh
```

This will start:
- MongoDB (Docker)
- Backend API (http://localhost:8000)
- Frontend (http://localhost:5173)

### Initialize with UNC Course Data

To populate the database with real UNC course data for testing:

```bash
# Initialize database with sample UNC courses and ratings
./scripts/initialize_db.sh
```

This adds:
- **8 UNC majors** (Art, Applied Sciences, Biology, Computer Science, Data Science, Economics, Business Administration, Neuroscience)
- **288+ real UNC courses** with actual course codes and names
- **580+ class difficulty ratings** (1-10 scale)
- **1,280+ professor reviews** with realistic ratings
- **40 sample professors** teaching across different courses

## Usage

1. **Register/Login:** Use your UNC email address to create an account
2. **Choose Major:** Select your major from the homepage
3. **Browse Ratings:** View class difficulty rankings and professor ratings
4. **Submit Ratings:** Rate classes and professors you've experienced
5. **Search:** Find specific classes using the search functionality

## API Endpoints

### Authentication
- `POST /auth/register` - Register new UNC student
- `POST /auth/login` - Login with email/password
- `GET /auth/me` - Get current user profile

### Ratings & Data
- `GET /majors` - Get all available majors
- `GET /majors/{major}/classes` - Get class rankings by major
- `POST /submissions/difficulty` - Submit class difficulty rating
- `POST /submissions/professor` - Submit professor rating
- `GET /professors/{professor}/ratings` - Get professor ratings

## Development

The application follows a modern full-stack architecture:
- React frontend with component-based design
- FastAPI backend with dependency injection
- MongoDB with proper indexing for performance
- JWT-based authentication with secure password storage

## License

Educational use for UNC students.
