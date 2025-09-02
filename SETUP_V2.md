# StudySync V2 Setup Guide

## 🚀 New Features Overview

StudySync V2 is a complete revamp of the original schedule maker with these new features:

- **UNC Email Authentication**: Users must sign up with a UNC email (@unc.edu, @live.unc.edu, @ad.unc.edu)
- **Major-Based Navigation**: Users are displayed as "Major YYYY" (e.g., "Computer Science 2028")
- **Class Difficulty Rankings**: See which classes are hardest based on user ratings (1-10 scale)
- **Professor Ratings**: Rate and view professor ratings with reviews
- **Major-Specific Pages**: Explore any major's class rankings and professor feedback
- **Modern UI**: Clean, responsive design with UNC branding

## 🛠️ Quick Setup

### Option 1: Automated Setup (Recommended)

```bash
# Run the automated setup script
./start_new.sh
```

This will:
- Start MongoDB (via Docker or remind you to start it manually)
- Set up Python virtual environment and install dependencies
- Create .env file from template
- Start both backend and frontend servers

### Option 2: Manual Setup

#### 1. Database Setup

**MongoDB via Docker (Recommended):**
```bash
docker-compose up -d mongodb
```

**MongoDB via Homebrew:**
```bash
brew install mongodb-community
brew services start mongodb-community
```

#### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env and set your JWT_SECRET_KEY

# Start the new backend server
uvicorn new_main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## 🌐 Access Points

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📊 Database Schema

### Collections

1. **users**
   ```javascript
   {
     _id: ObjectId,
     email: "student@unc.edu",
     major: "Computer Science",
     grad_year: 2028,
     display_name: "Computer Science 2028",
     created_at: ISODate,
     is_active: true
   }
   ```

2. **class_submissions**
   ```javascript
   {
     _id: ObjectId,
     class_code: "COMP 550",
     class_name: "Algorithms and Data Structures",
     major: "Computer Science",
     difficulty_rating: 8,
     professor: "Dr. Smith",
     semester: "Fall 2024",
     user_id: "user_object_id",
     submitted_at: ISODate
   }
   ```

3. **professor_ratings**
   ```javascript
   {
     _id: ObjectId,
     professor: "Dr. Smith",
     class_code: "COMP 550",
     rating: 4.5,
     review: "Great professor, explains concepts clearly",
     major: "Computer Science",
     semester: "Fall 2024",
     user_id: "user_object_id",
     submitted_at: ISODate
   }
   ```

## 🔐 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user profile

### Majors & Classes
- `GET /majors` - Get all majors
- `GET /majors/{major}/stats` - Get major statistics
- `GET /majors/{major}/classes` - Get class rankings for major

### Submissions
- `POST /submissions/difficulty` - Submit class difficulty rating
- `POST /submissions/professor` - Submit professor rating

### Professors
- `GET /professors/{professor}/ratings` - Get professor ratings

## 🎯 User Flow

1. **Registration/Login**: User enters UNC email, major, and graduation year
2. **Major Selection**: Homepage shows all majors with statistics
3. **Class Rankings**: Click on a major to see difficulty rankings
4. **Professor Ratings**: View professor ratings for each class
5. **Submit Ratings**: Users can rate class difficulty and professors (only for their major)

## 🔧 Configuration

### Environment Variables (backend/.env)

```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=schedulemaker_v2

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
```

### Security Notes

- JWT tokens expire after 7 days
- Users can only submit ratings for their own major
- UNC email validation is enforced
- All input is validated and sanitized

## 🚀 Migration from V1

To migrate from the original StudySync:

1. **Data Migration**: The new system uses different collections, so existing schedule/note data won't transfer automatically
2. **User Accounts**: All users need to re-register with the new authentication system
3. **Functionality**: The schedule optimization features are replaced with class rating features

## 🐛 Troubleshooting

### Common Issues

1. **MongoDB Connection Failed**
   - Ensure MongoDB is running: `brew services start mongodb-community`
   - Check connection string in `.env` file

2. **JWT Token Issues**
   - Set a secure JWT_SECRET_KEY in backend/.env
   - Clear browser localStorage if having auth issues

3. **CORS Issues**
   - Backend is configured for localhost:5173 and localhost:3000
   - Adjust CORS settings in new_main.py if using different ports

4. **Module Not Found Errors**
   - Ensure virtual environment is activated: `source backend/venv/bin/activate`
   - Reinstall dependencies: `pip install -r requirements.txt`

## 📝 Development Notes

### File Structure
```
StudySync/
├── backend/
│   ├── new_main.py          # New FastAPI application
│   ├── auth_models.py       # Pydantic models for auth & ratings
│   ├── database.py          # Database operations
│   ├── mongo_db.py          # MongoDB connection (existing)
│   ├── requirements.txt     # Updated dependencies
│   └── .env                 # Environment configuration
├── frontend/
│   └── src/
│       ├── App.jsx          # Updated main app component
│       └── components/
│           ├── Login.jsx    # Authentication component
│           ├── MajorSelection.jsx  # Major selection homepage
│           └── MajorPage.jsx       # Class rankings page
└── start_new.sh             # Automated startup script
```

### Key Libraries Added
- **Backend**: pyjwt[crypto], bcrypt, python-multipart
- **Frontend**: No new dependencies (uses existing React + Axios)

## 🔄 Running Both Versions

To run the original StudySync alongside V2:

**Original version:**
```bash
./start.sh  # Uses port 8000 for backend
```

**New version:**
```bash
./start_new.sh  # Uses port 8001 for backend (update if needed)
```

Make sure to use different database names in the .env files to avoid conflicts.