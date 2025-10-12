#!/usr/bin/env python3
"""
Database Configuration Test Script

This script helps you test different database configurations and
verify that the connection works with your chosen database name.
"""

import os
from dotenv import load_dotenv
from config import Config
from models.database import mongo
from flask import Flask

def test_db_connection(db_name=None):
    """Test database connection with optional database name override"""
    
    # Load environment variables
    load_dotenv()
    
    # Override database name if provided
    if db_name:
        os.environ['MONGO_DB_NAME'] = db_name
        print(f"🔄 Testing with database name: {db_name}")
    else:
        print(f"🔄 Testing with database name from .env: {Config.MONGO_DB_NAME}")
    
    # Create Flask app for testing
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize MongoDB
    mongo.init_app(app)
    
    try:
        with app.app_context():
            # Test connection by trying to access database info
            db_name_used = mongo.db.name
            collections = mongo.db.list_collection_names()
            
            print("✅ Database connection successful!")
            print(f"📊 Connected to database: {db_name_used}")
            print(f"📁 Available collections: {collections if collections else 'No collections yet'}")
            
            # Test basic operations
            test_collection = mongo.db.test_connection
            
            # Insert a test document
            test_doc = {"test": True, "message": "Database configuration working!"}
            result = test_collection.insert_one(test_doc)
            print(f"✅ Test document inserted with ID: {result.inserted_id}")
            
            # Read it back
            found_doc = test_collection.find_one({"_id": result.inserted_id})
            if found_doc:
                print("✅ Test document retrieved successfully")
            
            # Clean up test document
            test_collection.delete_one({"_id": result.inserted_id})
            print("🧹 Test document cleaned up")
            
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False

def show_config():
    """Display current database configuration"""
    print("\n" + "="*50)
    print("📋 CURRENT DATABASE CONFIGURATION")
    print("="*50)
    print(f"MONGO_HOST: {Config.MONGO_HOST}")
    print(f"MONGO_DB_NAME: {Config.MONGO_DB_NAME}")
    print(f"MONGO_URI: {Config.MONGO_URI}")
    print("="*50 + "\n")

def main():
    """Main function"""
    print("🚀 Aid Management System - Database Configuration Test\n")
    
    show_config()
    
    # Test current configuration
    print("Testing current configuration...")
    success = test_db_connection()
    
    if success:
        print("\n🎉 Your database configuration is working perfectly!")
        print("You can now run your application with: python app.py")
    else:
        print("\n⚠️  Please check your database configuration in .env file")
        print("Make sure your MONGO_HOST and MONGO_DB_NAME are correct")
    
    print("\n💡 To change database name:")
    print("1. Edit .env file and change MONGO_DB_NAME=your_new_db_name")
    print("2. Or run: python test_db_config.py your_new_db_name")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Test with provided database name
        db_name = sys.argv[1]
        show_config()
        test_db_connection(db_name)
    else:
        main()