from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.database import AidRequest, User
from functools import wraps
from bson.objectid import ObjectId

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
    """Approve an aid request (redirects to payment gateway)"""
    # Redirect to payment gateway instead of direct approval
    return redirect(url_for('payment.payment_gateway', request_id=request_id))

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

@aid_bp.route('/my-donations')
@login_required
@role_required(['donor', 'admin'])
def my_donations():
    """View donor's donation history"""
    donations = AidRequest.get_donor_contributions(session['user_id'])
    total_donated = AidRequest.get_donor_total_contribution(session['user_id'])
    
    # Enrich with beneficiary data
    for donation in donations:
        user = User.find_by_id(donation['user_id'])
        donation['user_name'] = user['name'] if user else 'Unknown'
        # Add request ID for reference in the template
        donation['request_id'] = str(donation['_id'])
    
    return render_template('my_donations.html', donations=donations, total_donated=total_donated)

@aid_bp.route('/complete-request/<request_id>')
@login_required
@role_required(['donor', 'admin'])
def complete_request(request_id):
    """Mark an aid request as completed"""
    AidRequest.update_status(request_id, 'completed', session['user_id'])
    flash('Request marked as completed', 'success')
    return redirect(url_for('aid.manage_requests'))

@aid_bp.route('/delete-request/<request_id>')
@login_required
def delete_request(request_id):
    """Delete an aid request"""
    # Get the request to check ownership
    aid_request = AidRequest.get_request_by_id(request_id)
    
    # Check if request exists
    if not aid_request:
        flash('Request not found', 'error')
        return redirect(url_for('aid.my_requests'))
    
    # Check if user is the owner of the request or an admin
    if str(aid_request['user_id']) != session['user_id'] and session['user_role'] != 'admin':
        flash('You do not have permission to delete this request', 'error')
        return redirect(url_for('aid.my_requests'))
    
    # Only allow deletion of pending requests
    if aid_request['status'] != 'pending':
        flash('Only pending requests can be deleted', 'error')
        return redirect(url_for('aid.my_requests'))
    
    # Delete the request
    AidRequest.delete_request(request_id)
    flash('Request deleted successfully', 'success')
    return redirect(url_for('aid.my_requests'))
