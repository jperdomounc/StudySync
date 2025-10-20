// MongoDB initialization script for StudySync
// This script runs when MongoDB container starts for the first time

// Switch to admin database for user creation
db = db.getSiblingDB('admin');

// Create application user
db.createUser({
  user: 'studysync',
  pwd: 'studysync_password_change_in_production',
  roles: [
    {
      role: 'readWrite',
      db: 'studysync'
    }
  ]
});

// Switch to application database
db = db.getSiblingDB('studysync');

// Create collections with proper indexes
db.createCollection('users');
db.createCollection('class_submissions'); 
db.createCollection('professor_ratings');

// Create indexes for better performance
// Users collection indexes
db.users.createIndex({ "email": 1 }, { unique: true });
db.users.createIndex({ "major": 1 });
db.users.createIndex({ "grad_year": 1 });

// Class submissions indexes
db.class_submissions.createIndex({ "major": 1, "class_code": 1 });
db.class_submissions.createIndex({ "class_code": 1, "major": 1 });
db.class_submissions.createIndex({ "user_id": 1 });
db.class_submissions.createIndex({ "professor": 1 });
db.class_submissions.createIndex({ "submitted_at": 1 });

// Professor ratings indexes
db.professor_ratings.createIndex({ "professor": 1, "class_code": 1 });
db.professor_ratings.createIndex({ "major": 1, "professor": 1 });
db.professor_ratings.createIndex({ "user_id": 1 });
db.professor_ratings.createIndex({ "submitted_at": 1 });

// Compound indexes for common queries
db.class_submissions.createIndex({ "major": 1, "class_code": 1, "user_id": 1 });
db.professor_ratings.createIndex({ "professor": 1, "class_code": 1, "user_id": 1 });

print('StudySync database initialization completed');