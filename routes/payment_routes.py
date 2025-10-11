from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.database import AidRequest, User
from functools import wraps
from bson.objectid import ObjectId

payment_bp = Blueprint('payment', __name__)

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

@payment_bp.route('/payment-gateway/<request_id>')
@login_required
@role_required(['donor', 'admin'])
def payment_gateway(request_id):
    """Mock payment gateway for donors"""
    # Get the aid request
    aid_request = AidRequest.get_request_by_id(request_id)
    
    # Check if request exists
    if not aid_request:
        flash('Request not found', 'error')
        return redirect(url_for('aid.manage_requests'))
    
    # Check if request is pending
    if aid_request['status'] != 'pending':
        flash('This request is no longer pending', 'error')
        return redirect(url_for('aid.manage_requests'))
    
    # Get beneficiary information
    beneficiary = User.find_by_id(aid_request['user_id'])
    
    # Check if beneficiary has bank account information
    if not beneficiary.get('bank_account'):
        flash('Beneficiary has not provided bank account information yet', 'error')
        return redirect(url_for('aid.manage_requests'))
    
    return render_template('payment_gateway.html', 
                          request=aid_request, 
                          beneficiary=beneficiary)

@payment_bp.route('/process-payment/<request_id>', methods=['POST'])
@login_required
@role_required(['donor', 'admin'])
def process_payment(request_id):
    """Process the mock payment"""
    # Get the aid request
    aid_request = AidRequest.get_request_by_id(request_id)
    
    # Check if request exists
    if not aid_request:
        flash('Request not found', 'error')
        return redirect(url_for('aid.manage_requests'))
    
    # Check if request is pending
    if aid_request['status'] != 'pending':
        flash('This request is no longer pending', 'error')
        return redirect(url_for('aid.manage_requests'))
    
    # Get payment method from form
    payment_method = request.form.get('payment_method')
    
    if not payment_method:
        flash('Please select a payment method', 'error')
        return redirect(url_for('payment.payment_gateway', request_id=request_id))
    
    # In a real application, we would process the payment here
    # For this mock implementation, we'll just approve the request
    
    # Update the request status to approved
    AidRequest.update_status(request_id, 'approved', session['user_id'])
    
    flash('Payment processed successfully! The request has been approved.', 'success')
    return redirect(url_for('aid.my_donations'))