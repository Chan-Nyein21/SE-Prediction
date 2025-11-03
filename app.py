from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import timedelta

app = Flask(__name__)

# Secret key for session management
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')
app.permanent_session_lifetime = timedelta(hours=2)

# MySQL Configuration
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'se_prediction_db')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize MySQL
mysql = MySQL(app)

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
    
    # Query database for user
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    
    if user and check_password_hash(user['password'], password):
        session.permanent = True
        session['user_id'] = user['id']
        session['email'] = user['email']
        session['role'] = user['role']
        
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
    
    # Create new user
    hashed_password = generate_password_hash(password)
    cur.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
                (name, email, hashed_password, 'user'))
    mysql.connection.commit()
    cur.close()
    
    flash('Registration successful! Please login.', 'success')
    return redirect(url_for('login'))

@app.route('/user/dashboard')
def user_dashboard():
    """User dashboard page"""
    if 'user_id' not in session or session.get('role') != 'user':
        flash('Please login to access this page', 'error')
        return redirect(url_for('login'))
    
    return render_template('user/dashboard.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard page"""
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    return render_template('admin/dashboard.html')

@app.route('/logout')
def logout():
    """Logout user and clear session"""
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
