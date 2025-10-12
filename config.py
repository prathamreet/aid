import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # MongoDB Configuration
    MONGO_HOST = os.environ.get('MONGO_HOST') or 'mongodb://localhost:27017'
    MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME') or 'micro_lending_db'
    
    # Legacy MONGO_URI support (for backward compatibility)
    # If MONGO_URI is provided, it takes precedence
    _mongo_uri = os.environ.get('MONGO_URI')
    if _mongo_uri:
        # Extract database name from URI if not explicitly provided
        if '/' in _mongo_uri and not os.environ.get('MONGO_DB_NAME'):
            try:
                # Extract database name from the URI
                db_part = _mongo_uri.split('/')[-1]
                if '?' in db_part:
                    db_part = db_part.split('?')[0]
                if db_part:
                    MONGO_DB_NAME = db_part
            except:
                pass
        
        # Remove database name from URI to construct base host
        if '/' in _mongo_uri:
            MONGO_HOST = '/'.join(_mongo_uri.split('/')[:-1])
        else:
            MONGO_HOST = _mongo_uri
    
    # Construct the final URI
    MONGO_URI = f"{MONGO_HOST}/{MONGO_DB_NAME}"
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes
