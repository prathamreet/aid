from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.database import AidRequest, User
from functools import wraps

aid_bp = Blueprint('aid', __name__)

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(roles):
    """Decorator to require specific role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get('user_role') not in roles:
                flash('You do not have permission to access this page', 'error')
                return redirect(url_for('dashboard.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@aid_bp.route('/request-aid', methods=['GET', 'POST'])
@login_required
@role_required(['beneficiary', 'admin'])
def request_aid():
    """Create new aid request"""
    if request.method == 'POST':
        purpose = request.form.get('purpose')
        amount = request.form.get('amount')
        category = request.form.get('category')
        
        # Validation
        if not all([purpose, amount, category]):
            flash('All fields are required', 'error')
            return redirect(url_for('aid.request_aid'))
        
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            flash('Please enter a valid amount', 'error')
            return redirect(url_for('aid.request_aid'))
        
        # Create request
        AidRequest.create_request(session['user_id'], purpose, amount, category)
        flash('Aid request submitted successfully!', 'success')
        return redirect(url_for('dashboard.index'))
    
    categories = ['Education', 'Health', 'Livelihood', 'Emergency', 'Other']
    return render_template('request_aid.html', categories=categories)

@aid_bp.route('/manage-requests')
@login_required
@role_required(['donor', 'admin'])
def manage_requests():
    """View and manage aid requests (for donors/admins)"""
    pending = AidRequest.get_pending_requests()
    
    # Enrich with user data
    for req in pending:
        user = User.find_by_id(req['user_id'])
        req['user_name'] = user['name'] if user else 'Unknown'
    
    return render_template('manage_requests.html', requests=pending)

@aid_bp.route('/approve-request/<request_id>')
@login_required
@role_required(['donor', 'admin'])
def approve_request(request_id):
    """Approve an aid request"""
    AidRequest.update_status(request_id, 'approved', session['user_id'])
    flash('Request approved successfully', 'success')
    return redirect(url_for('aid.manage_requests'))

@aid_bp.route('/reject-request/<request_id>')
@login_required
@role_required(['donor', 'admin'])
def reject_request(request_id):
    """Reject an aid request"""
    AidRequest.update_status(request_id, 'rejected', session['user_id'])
    flash('Request rejected', 'info')
    return redirect(url_for('aid.manage_requests'))

@aid_bp.route('/my-requests')
@login_required
def my_requests():
    """View user's own requests"""
    requests = AidRequest.get_user_requests(session['user_id'])
    return render_template('my_requests.html', requests=requests)

@aid_bp.route('/complete-request/<request_id>')
@login_required
@role_required(['donor', 'admin'])
def complete_request(request_id):
    """Mark an aid request as completed"""
    AidRequest.update_status(request_id, 'completed', session['user_id'])
    flash('Request marked as completed', 'success')
    return redirect(url_for('aid.manage_requests'))
