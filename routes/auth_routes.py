from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.database import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration endpoint"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'beneficiary')
        
        # Validation
        if not all([name, email, password]):
            flash('All fields are required', 'error')
            return redirect(url_for('auth.register'))
        
        # Check if user exists
        if User.find_by_email(email):
            flash('Email already registered', 'error')
            return redirect(url_for('auth.register'))
        
        # Create user
        User.create_user(name, email, password, role)
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login endpoint"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.find_by_email(email)
        
        if user and User.verify_password(user, password):
            # Set session
            session['user_id'] = str(user['_id'])
            session['user_name'] = user['name']
            session['user_role'] = user['role']
            session.permanent = True
            
            flash(f'Welcome back, {user["name"]}!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('auth.login'))
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """User logout endpoint"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))
