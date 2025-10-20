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
            database_name = os.getenv("DATABASE_NAME", "studysync")
            
            # Production-ready connection options
            self.client = MongoClient(
                mongodb_url, 
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                maxPoolSize=50,
                retryWrites=True
            )
            self.db = self.client[database_name]
            
            # Test the connection
            self.client.admin.command('ping')
            print(f"✅ Connected to MongoDB: {database_name}")
            
        except Exception as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            print("Please ensure MongoDB is running or check MONGODB_URL in .env")
            raise
    
    def get_collection(self, collection_name: str):
        """Get a collection from the database"""
        return self.db[collection_name]
    
    def get_health_status(self):
        """Check database health for monitoring"""
        try:
            self.client.admin.command('ping')
            return {"status": "healthy", "database": self.db.name}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
    
    def close(self):
        """Close the database connection"""
        if self.client:
            self.client.close()

# Global database instance
mongo_db = MongoDatabase()