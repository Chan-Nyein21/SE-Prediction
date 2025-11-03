from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
from datetime import timedelta, datetime

app = Flask(__name__)

# Secret key for session management (must remain constant across restarts)
# Using a fixed secret key to maintain sessions across server restarts
app.secret_key = 'se-prediction-demo-secret-key-12345-fixed-for-persistent-sessions'

# Session configuration - Extended session lifetime
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_NAME'] = 'se_prediction_session'
app.config['SESSION_REFRESH_EACH_REQUEST'] = True  # Refresh session on each request
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)  # 30 days
app.permanent_session_lifetime = timedelta(days=30)

# File to store users data
USERS_FILE = 'demo_users.json'

def load_users():
    """Load users from file"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    # Return default admin user if file doesn't exist
    return {
        'admin@gmail.com': {
            'id': 1,
            'name': 'Admin',
            'email': 'admin@gmail.com',
            'password': generate_password_hash('admin'),
            'role': 'admin'
        }
    }

def save_users():
    """Save users to file"""
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(demo_users, f, indent=2)
    except Exception as e:
        print(f"Error saving users: {e}")

# Demo users (persistent across restarts)
demo_users = load_users()

# Keep sessions alive - extend session on every request
@app.before_request
def make_session_permanent():
    """Make all sessions permanent and refresh them on each request"""
    session.permanent = True
    session.modified = True
    
    # Debug: Print session info for every request
    if 'user_id' in session:
        session['last_activity'] = datetime.now().isoformat()
        print(f"[SESSION OK] User: {session.get('email')}, Role: {session.get('role')}, Path: {request.path}, Session ID: {session.get('user_id')}")
    else:
        print(f"[NO SESSION] Path: {request.path}, Cookies: {request.cookies.get('se_prediction_session', 'None')}")

# Routes
@app.route('/')
def index():
    """Welcome/Landing page"""
    return render_template('welcome.html')

@app.route('/login')
def login():
    """Login page for users"""
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    """Handle login form submission"""
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email or not password:
        flash('Please fill in all fields', 'error')
        return redirect(url_for('login'))
    
    # Check demo users
    user = demo_users.get(email)
    
    if user and check_password_hash(user['password'], password):
        # Check if user is pending approval (not admin)
        if user['role'] != 'admin' and user.get('status') == 'Pending':
            flash('Your account is pending admin approval. Please wait.', 'error')
            return redirect(url_for('login'))
        
        # Clear any existing session data first
        session.clear()
        
        # Set session as permanent BEFORE adding data
        session.permanent = True
        
        # Add user data to session
        session['user_id'] = user['id']
        session['email'] = user['email']
        session['name'] = user['name']
        session['role'] = user['role']
        session['login_time'] = datetime.now().isoformat()
        session['last_activity'] = datetime.now().isoformat()
        
        # Force session to be saved
        session.modified = True
        
        flash(f'Welcome back, {user["name"]}!', 'success')
        
        if user['role'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('user_dashboard'))
    else:
        flash('Invalid email or password', 'error')
        return redirect(url_for('login'))

@app.route('/register')
def register():
    """Registration page for new users"""
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    """Handle registration form submission"""
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    if not all([name, email, password, confirm_password]):
        flash('Please fill in all fields', 'error')
        return redirect(url_for('register'))
    
    if password != confirm_password:
        flash('Passwords do not match', 'error')
        return redirect(url_for('register'))
    
    # Check if user already exists
    if email in demo_users:
        flash('Email already registered', 'error')
        return redirect(url_for('register'))
    
    # Get current date for joined field
    from datetime import datetime
    joined_date = datetime.now().strftime('%Y-%m-%d')
    
    # Create new user with pending status (requires admin approval)
    demo_users[email] = {
        'id': len(demo_users) + 1,
        'name': name,
        'email': email,
        'password': generate_password_hash(password),
        'role': 'user',
        'status': 'Pending',  # Requires admin approval
        'joined': joined_date
    }
    
    save_users()  # Save to file
    
    flash('Registration successful! Please wait for admin approval.', 'success')
    return redirect(url_for('login'))

@app.route('/user/dashboard')
def user_dashboard():
    """User dashboard page"""
    if 'user_id' not in session or session.get('role') != 'user':
        flash('Please login to access this page', 'error')
        return redirect(url_for('login'))
    
    return render_template('user/dashboard.html')

@app.route('/user/analytics')
def analytics():
    """User analytics page"""
    if 'user_id' not in session or session.get('role') != 'user':
        flash('Please login to access this page', 'error')
        return redirect(url_for('login'))
    
    return render_template('user/analytics.html')

@app.route('/user/predict', methods=['GET', 'POST'])
def predict():
    """User predict page"""
    if 'user_id' not in session or session.get('role') != 'user':
        flash('Please login to access this page', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Handle file upload and prediction (will implement with ML model later)
        flash('Prediction completed successfully!', 'success')
        return redirect(url_for('predict'))
    
    return render_template('user/predict.html')

@app.route('/user/results')
def results():
    """User results page"""
    if 'user_id' not in session or session.get('role') != 'user':
        flash('Please login to access this page', 'error')
        return redirect(url_for('login'))
    
    return render_template('user/results.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard page"""
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    # Verify user still exists in database (in case of server restart)
    user_email = session.get('email')
    if user_email not in demo_users:
        session.clear()
        flash('Session expired. Please login again.', 'error')
        return redirect(url_for('login'))
    
    # Prepare user data for display (excluding admin)
    users_list = []
    for email, user in demo_users.items():
        if user['role'] != 'admin':
            # Generate initials from name
            name_parts = user['name'].split()
            initials = ''.join([part[0].upper() for part in name_parts[:2]])
            
            users_list.append({
                'username': user['name'],
                'email': user['email'],
                'status': user.get('status', 'Active'),
                'joined': user.get('joined', '2025-10-20'),
                'initials': initials
            })
    
    # Calculate statistics
    total_users = len(users_list)
    pending_users = sum(1 for u in users_list if u['status'] == 'Pending')
    active_users = sum(1 for u in users_list if u['status'] == 'Active')
    
    return render_template('admin/dashboard.html', 
                         users=users_list,
                         total_users=total_users,
                         pending_users=pending_users,
                         active_users=active_users)

@app.route('/admin/overview')
def admin_overview():
    """Admin overview page - enrollment statistics"""
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    return render_template('admin/overview.html')

@app.route('/admin/accept-user', methods=['POST'])
def accept_user():
    """Accept a pending user"""
    if 'user_id' not in session or session.get('role') != 'admin':
        return {'success': False, 'message': 'Access denied'}, 403
    
    data = request.get_json()
    email = data.get('email')
    
    if email in demo_users:
        demo_users[email]['status'] = 'Active'
        save_users()  # Save to file
        return {'success': True, 'message': 'User accepted successfully'}
    
    return {'success': False, 'message': 'User not found'}, 404

@app.route('/admin/delete-user', methods=['POST'])
def delete_user():
    """Delete a user"""
    if 'user_id' not in session or session.get('role') != 'admin':
        return {'success': False, 'message': 'Access denied'}, 403
    
    data = request.get_json()
    email = data.get('email')
    
    if email in demo_users and demo_users[email]['role'] != 'admin':
        del demo_users[email]
        save_users()  # Save to file
        return {'success': True, 'message': 'User deleted successfully'}
    
    return {'success': False, 'message': 'Cannot delete this user'}, 400

@app.route('/admin/predict', methods=['GET', 'POST'])
def admin_predict():
    """Admin predict page"""
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Handle file upload and prediction (will implement with ML model later)
        flash('Prediction completed successfully!', 'success')
        return redirect(url_for('admin_predict'))
    
    return render_template('admin/predict.html')

@app.route('/admin/results')
def admin_results():
    """Admin results page"""
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    return render_template('admin/results.html')

@app.route('/admin/analytics')
def admin_analytics():
    """Admin analytics page"""
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    return render_template('admin/analytics.html')

@app.route('/logout')
def logout():
    """Logout user and clear session"""
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return f"<h1>404 - Page Not Found</h1><p>The page you're looking for doesn't exist.</p>", 404

@app.errorhandler(500)
def server_error(e):
    return f"<h1>500 - Server Error</h1><p>Something went wrong on our end.</p>", 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 SE Prediction System - Demo Mode")
    print("="*60)
    print("\n📱 Server running at: http://localhost:5001")
    print("\n👥 Demo Credentials:")
    print("   Admin: admin@gmail.com / admin")
    print("   User:  user@example.com / user123")
    print("\n⚠️  Note: Using file-based storage (demo_users.json)")
    print("="*60 + "\n")
    
    # Run with use_reloader=False to prevent automatic restarts that clear sessions
    app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)
