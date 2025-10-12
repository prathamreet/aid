#!/usr/bin/env python3
"""
Database Management Script

This script provides easy database management operations:
- Switch between databases
- View database contents
- Create admin users
- Reset database
"""

import os
import sys
from dotenv import load_dotenv, set_key
from config import Config
from models.database import mongo, User, AidRequest
from flask import Flask

def create_app_context():
    """Create Flask application context for database operations"""
    app = Flask(__name__)
    app.config.from_object(Config)
    mongo.init_app(app)
    return app

def switch_database(db_name):
    """Switch to a different database"""
    env_path = '.env'
    
    # Update the .env file
    set_key(env_path, 'MONGO_DB_NAME', db_name)
    
    print(f"✅ Database switched to: {db_name}")
    print("🔄 Please restart the application for changes to take effect")
    
    # Test the new connection
    os.environ['MONGO_DB_NAME'] = db_name  # Update for current session
    app = create_app_context()
    
    with app.app_context():
        try:
            collections = mongo.db.list_collection_names()
            print(f"📊 Connected to database: {mongo.db.name}")
            print(f"📁 Collections: {collections if collections else 'No collections yet'}")
        except Exception as e:
            print(f"❌ Error connecting to new database: {str(e)}")

def view_database():
    """View current database contents"""
    app = create_app_context()
    
    with app.app_context():
        print(f"\n📊 Database: {mongo.db.name}")
        print("=" * 50)
        
        # Count users by role
        total_users = mongo.db.users.count_documents({})
        donors = mongo.db.users.count_documents({'role': 'donor'})
        beneficiaries = mongo.db.users.count_documents({'role': 'beneficiary'})
        admins = mongo.db.users.count_documents({'role': 'admin'})
        
        print(f"👥 Users: {total_users} total")
        print(f"   - Donors: {donors}")
        print(f"   - Beneficiaries: {beneficiaries}")
        print(f"   - Admins: {admins}")
        
        # Count aid requests by status
        total_requests = mongo.db.aid_requests.count_documents({})
        pending = mongo.db.aid_requests.count_documents({'status': 'pending'})
        approved = mongo.db.aid_requests.count_documents({'status': 'approved'})
        rejected = mongo.db.aid_requests.count_documents({'status': 'rejected'})
        completed = mongo.db.aid_requests.count_documents({'status': 'completed'})
        
        print(f"\n🎯 Aid Requests: {total_requests} total")
        print(f"   - Pending: {pending}")
        print(f"   - Approved: {approved}")
        print(f"   - Rejected: {rejected}")
        print(f"   - Completed: {completed}")
        
        # Calculate total aid amount
        pipeline = [
            {'$group': {
                '_id': '$status',
                'total_amount': {'$sum': '$amount'},
                'count': {'$sum': 1}
            }}
        ]
        
        amounts = list(mongo.db.aid_requests.aggregate(pipeline))
        if amounts:
            print(f"\n💰 Aid Amounts by Status:")
            for item in amounts:
                status = item['_id']
                total = item['total_amount']
                count = item['count']
                print(f"   - {status.capitalize()}: ₹{total:,.2f} ({count} requests)")

def create_admin_user(name=None, email=None, password=None):
    """Create an admin user"""
    app = create_app_context()
    
    with app.app_context():
        if not name:
            name = input("Enter admin name: ")
        if not email:
            email = input("Enter admin email: ")
        if not password:
            import getpass
            password = getpass.getpass("Enter admin password: ")
        
        # Check if user already exists
        existing_user = User.find_by_email(email)
        if existing_user:
            print(f"❌ User with email {email} already exists!")
            return False
        
        try:
            User.create_user(name, email, password, role='admin')
            print(f"✅ Admin user created successfully!")
            print(f"   Name: {name}")
            print(f"   Email: {email}")
            print(f"   Role: admin")
            return True
        except Exception as e:
            print(f"❌ Error creating admin user: {str(e)}")
            return False

def reset_database():
    """Reset the database (DANGER: Deletes all data!)"""
    app = create_app_context()
    
    with app.app_context():
        db_name = mongo.db.name
        
        confirm = input(f"⚠️  WARNING: This will delete ALL data in database '{db_name}'!\n"
                       f"Type 'DELETE {db_name}' to confirm: ")
        
        if confirm == f'DELETE {db_name}':
            try:
                # Drop all collections
                collections = mongo.db.list_collection_names()
                for collection in collections:
                    mongo.db[collection].drop()
                
                print(f"✅ Database '{db_name}' has been reset!")
                print("🔄 All collections have been dropped.")
            except Exception as e:
                print(f"❌ Error resetting database: {str(e)}")
        else:
            print("❌ Database reset cancelled.")

def main():
    """Main function"""
    load_dotenv()
    
    if len(sys.argv) < 2:
        print("🗃️  Aid Management System - Database Management")
        print("=" * 50)
        print("Usage: python manage_db.py <command> [options]")
        print("\nCommands:")
        print("  switch <db_name>    Switch to different database")
        print("  view               View current database contents")
        print("  create-admin       Create an admin user")
        print("  reset              Reset database (delete all data)")
        print("  config             Show current configuration")
        print("\nExamples:")
        print("  python manage_db.py switch mydb1")
        print("  python manage_db.py view")
        print("  python manage_db.py create-admin")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'switch':
        if len(sys.argv) < 3:
            print("❌ Please provide database name: python manage_db.py switch <db_name>")
            return
        db_name = sys.argv[2]
        switch_database(db_name)
    
    elif command == 'view':
        view_database()
    
    elif command == 'create-admin':
        create_admin_user()
    
    elif command == 'reset':
        reset_database()
    
    elif command == 'config':
        print("📋 Current Database Configuration")
        print("=" * 40)
        print(f"MONGO_HOST: {Config.MONGO_HOST}")
        print(f"MONGO_DB_NAME: {Config.MONGO_DB_NAME}")
        print(f"MONGO_URI: {Config.MONGO_URI}")
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Run 'python manage_db.py' for help")

if __name__ == "__main__":
    main()