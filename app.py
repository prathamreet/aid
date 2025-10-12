from flask import Flask, render_template
from config import Config
from models.database import mongo
from routes.auth_routes import auth_bp
from routes.aid_routes import aid_bp
from routes.dashboard_routes import dashboard_bp
from routes.profile_routes import profile_bp
from routes.payment_routes import payment_bp

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize MongoDB
    mongo.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(aid_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(payment_bp)
    
    # Home route
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

# Create app instance for Gunicorn
app = create_app()

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
