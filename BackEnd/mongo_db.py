"""MongoDB database connection and configuration"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class MongoDatabase:
    def __init__(self):
        self.client = None
        self.db = None
        self.connect()
    
    def connect(self):
        """Connect to MongoDB"""
        try:
            mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
            database_name = os.getenv("DATABASE_NAME", "schedulemaker")
            
            self.client = MongoClient(mongodb_url, serverSelectionTimeoutMS=5000)
            self.db = self.client[database_name]
            
            # Test the connection
            self.client.admin.command('ping')
            print(f"Connected to MongoDB at {mongodb_url}")
            
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            print("Please ensure MongoDB is running locally or update MONGODB_URL in .env")
            print("To start MongoDB locally: brew services start mongodb-community")
            raise
    
    def get_collection(self, collection_name: str):
        """Get a collection from the database"""
        return self.db[collection_name]
    
    def close(self):
        """Close the database connection"""
        if self.client:
            self.client.close()

# Global database instance
mongo_db = MongoDatabase()