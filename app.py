from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import timedelta, datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Secret key for session management
app.secret_key = os.environ.get('SECRET_KEY', 'se-prediction-secret-key-12345-fixed-for-persistent-sessions')

# Session configuration - Extended session lifetime
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('SESSION_COOKIE_SECURE', 'False') == 'True'
app.config['SESSION_COOKIE_HTTPONLY'] = os.environ.get('SESSION_COOKIE_HTTPONLY', 'True') == 'True'
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_NAME'] = 'se_prediction_session'
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
app.permanent_session_lifetime = timedelta(days=30)

# MySQL Configuration
app.config['MYSQL_HOST'] = os.environ.get('DB_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('DB_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('DB_PASSWORD', '')
app.config['MYSQL_DB'] = os.environ.get('DB_NAME', 'se_prediction_db')
app.config['MYSQL_PORT'] = int(os.environ.get('DB_PORT', 3306))
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize MySQL
mysql = MySQL(app)

# Keep sessions alive - extend session on every request
@app.before_request
def make_session_permanent():
    """Make all sessions permanent and refresh them on each request"""
    session.permanent = True
    session.modified = True
    
    # Update last activity time
    if 'user_id' in session:
        session['last_activity'] = datetime.now().isoformat()

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
    remember_me = request.form.get('remember')  # Get "Remember me" checkbox value
    
    if not email or not password:
        flash('Please fill in all fields', 'error')
        return redirect(url_for('login'))
    
    # Query database for user
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    
    if user and check_password_hash(user['password'], password):
        # Check if user is pending approval (not admin)
        if user['role'] != 'admin' and user.get('status') == 'Pending':
            flash('Your account is pending admin approval. Please wait.', 'error')
            cur.close()
            return redirect(url_for('login'))
        
        # Check if user is rejected
        if user.get('status') == 'Rejected':
            flash('Your account has been rejected. Please contact admin.', 'error')
            cur.close()
            return redirect(url_for('login'))
        
        # Clear any existing session data first
        session.clear()
        
        # Set session as permanent based on "Remember me" checkbox
        if remember_me:
            session.permanent = True  # Session lasts 30 days (as configured)
        else:
            session.permanent = False  # Session expires when browser closes
        
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
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cur.fetchone()
    
    if existing_user:
        flash('Email already registered', 'error')
        cur.close()
        return redirect(url_for('register'))
    
    # Create new user with Pending status (requires admin approval)
    hashed_password = generate_password_hash(password)
    cur.execute("INSERT INTO users (name, email, password, role, status) VALUES (%s, %s, %s, %s, %s)",
                (name, email, hashed_password, 'user', 'Pending'))
    mysql.connection.commit()
    cur.close()
    
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
    """Admin dashboard page - User management"""
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    # Get all users except admins from database
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, email, role, status, created_at FROM users WHERE role != 'admin' ORDER BY created_at DESC")
    users = cur.fetchall()
    cur.close()
    
    # Prepare user data for display
    users_list = []
    for user in users:
        # Generate initials from name
        name_parts = user['name'].split()
        initials = ''.join([part[0].upper() for part in name_parts[:2]])
        
        users_list.append({
            'username': user['name'],
            'email': user['email'],
            'status': user.get('status', 'Active'),  # Get status from database
            'joined': user['created_at'].strftime('%Y-%m-%d') if user['created_at'] else '',
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
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'success': False, 'message': 'Email required'}), 400
    
    try:
        cur = mysql.connection.cursor()
        # Update user status to Active
        cur.execute("UPDATE users SET status = 'Active' WHERE email = %s AND role != 'admin'", (email,))
        mysql.connection.commit()
        
        if cur.rowcount > 0:
            cur.close()
            return jsonify({'success': True, 'message': 'User approved successfully'})
        else:
            cur.close()
            return jsonify({'success': False, 'message': 'User not found or cannot be approved'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin/delete-user', methods=['POST'])
def delete_user():
    """Delete a user"""
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'success': False, 'message': 'Email required'}), 400
    
    try:
        cur = mysql.connection.cursor()
        # Don't allow deleting admin users
        cur.execute("DELETE FROM users WHERE email = %s AND role != 'admin'", (email,))
        mysql.connection.commit()
        
        if cur.rowcount > 0:
            cur.close()
            return jsonify({'success': True, 'message': 'User deleted successfully'})
        else:
            cur.close()
            return jsonify({'success': False, 'message': 'Cannot delete this user'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

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
    print("🚀 SE Prediction System - MySQL Mode")
    print("="*60)
    print("\n📱 Server running at: http://localhost:5002")
    print("\n👥 Default Credentials:")
    print("   Admin: admin@se-prediction.com / admin123")
    print("   User:  user@example.com / user123")
    print("\n💾 Using MySQL Database: se_prediction_db")
    print("="*60 + "\n")
    
    # Run with use_reloader=False to prevent automatic restarts that clear sessions
    app.run(debug=True, host='0.0.0.0', port=5002, use_reloader=False)
