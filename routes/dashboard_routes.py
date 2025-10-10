from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify
from utils.analytics import Analytics
from functools import wraps

dashboard_bp = Blueprint('dashboard', __name__)

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@dashboard_bp.route('/dashboard')
@login_required
def index():
    """Main dashboard view"""
    user_id = session.get('user_id')
    stats = Analytics.get_dashboard_stats(user_id)
    user_role = session.get('user_role')
    
    return render_template('dashboard.html', stats=stats, role=user_role)

@dashboard_bp.route('/api/chart-data')
@login_required
def chart_data():
    """API endpoint for chart data"""
    data = Analytics.get_category_chart_data()
    return jsonify(data)
