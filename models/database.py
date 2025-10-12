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
            'created_at': datetime.utcnow(),
            'bank_account': None,  # For beneficiaries to receive payments
            'bank_name': None,
            'account_holder': None
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
        
    @staticmethod
    def update_profile(user_id, update_data):
        """Update user profile information"""
        return mongo.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_data}
        )


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
    def get_donor_contributions(donor_id):
        """Get all requests approved or completed by a specific donor"""
        return list(mongo.db.aid_requests.find({
            'approved_by': ObjectId(donor_id),
            'status': {'$in': ['approved', 'completed']}
        }))
    
    @staticmethod
    def get_donor_total_contribution(donor_id):
        """Get total amount donated by a specific donor"""
        pipeline = [
            {'$match': {
                'approved_by': ObjectId(donor_id),
                'status': {'$in': ['approved', 'completed']}
            }},
            {'$group': {
                '_id': None,
                'total': {'$sum': '$amount'}
            }}
        ]
        result = list(mongo.db.aid_requests.aggregate(pipeline))
        return result[0]['total'] if result else 0
    
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
        
    @staticmethod
    def delete_request(request_id):
        """Delete an aid request by ID"""
        return mongo.db.aid_requests.delete_one({'_id': ObjectId(request_id)})
    
    
