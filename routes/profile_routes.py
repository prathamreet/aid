from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.database import User
from functools import wraps
from bson.objectid import ObjectId

profile_bp = Blueprint('profile', __name__)

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@profile_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def view_profile():
    """View and edit user profile"""
    user = User.find_by_id(session['user_id'])
    
    if request.method == 'POST':
        # Update basic profile information
        update_data = {
            'name': request.form.get('name')
        }
        
        # If user is a beneficiary, update bank account information
        if user['role'] == 'beneficiary':
            update_data.update({
                'bank_account': request.form.get('bank_account'),
                'bank_name': request.form.get('bank_name'),
                'account_holder': request.form.get('account_holder')
            })
        
        # Update the user profile
        User.update_profile(session['user_id'], update_data)
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile.view_profile'))
    
    return render_template('profile.html', user=user)