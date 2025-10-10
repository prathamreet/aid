from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from bson.objectid import ObjectId

mongo = PyMongo()

class User:
    """User model for authentication and role management"""
    
    @staticmethod
    def create_user(name, email, password, role='beneficiary'):
        """Create a new user with hashed password"""
        user = {
            'name': name,
            'email': email.lower(),
            'password_hash': generate_password_hash(password),
            'role': role,  # donor, beneficiary, admin
            'created_at': datetime.utcnow()
        }
        return mongo.db.users.insert_one(user)
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        return mongo.db.users.find_one({'email': email.lower()})
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        return mongo.db.users.find_one({'_id': ObjectId(user_id)})
    
    @staticmethod
    def verify_password(user, password):
        """Verify user password"""
        return check_password_hash(user['password_hash'], password)
    
    @staticmethod
    def get_all_donors():
        """Get all donor users"""
        return list(mongo.db.users.find({'role': 'donor'}))
    
    @staticmethod
    def get_all_beneficiaries():
        """Get all beneficiary users"""
        return list(mongo.db.users.find({'role': 'beneficiary'}))


class AidRequest:
    """Aid request model for loan/aid management"""
    
    @staticmethod
    def create_request(user_id, purpose, amount, category):
        """Create new aid request"""
        request = {
            'user_id': ObjectId(user_id),
            'purpose': purpose,
            'amount': float(amount),
            'category': category,  # Education, Health, Livelihood, Emergency, Other
            'status': 'pending',  # pending, approved, rejected, completed
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'approved_by': None
        }
        return mongo.db.aid_requests.insert_one(request)
    
    @staticmethod
    def get_all_requests():
        """Get all aid requests"""
        return list(mongo.db.aid_requests.find())
    
    @staticmethod
    def get_pending_requests():
        """Get pending aid requests"""
        return list(mongo.db.aid_requests.find({'status': 'pending'}))
    
    @staticmethod
    def get_user_requests(user_id):
        """Get requests by specific user"""
        return list(mongo.db.aid_requests.find({'user_id': ObjectId(user_id)}))
    
    @staticmethod
    def update_status(request_id, status, donor_id=None):
        """Update request status"""
        update_data = {
            'status': status,
            'updated_at': datetime.utcnow()
        }
        if donor_id:
            update_data['approved_by'] = ObjectId(donor_id)
        
        return mongo.db.aid_requests.update_one(
            {'_id': ObjectId(request_id)},
            {'$set': update_data}
        )
    
    @staticmethod
    def get_request_by_id(request_id):
        """Get single request by ID"""
        return mongo.db.aid_requests.find_one({'_id': ObjectId(request_id)})
