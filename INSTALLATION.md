# 🎓 SE Enrollment Prediction System - Installation Guide for IT Department

## Overview
This system is designed for university use to predict Software Engineering student enrollment. It requires one-time setup by the IT department.

---

## 📋 Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- Git

---

## 🚀 Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/Chan-Nyein21/SE-Prediction.git
cd SE-Prediction
```

### Step 2: Set Up Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Configure Database

#### Option A: Customize Admin Credentials BEFORE Database Setup (Recommended)

1. **Generate your admin password hash:**

```bash
python3 -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('YOUR_ADMIN_PASSWORD_HERE'))"
```

2. **Edit `database_schema.sql`:**
   - Open the file in a text editor
   - Find the line that starts with `INSERT INTO users` (for admin)
   - Replace:
     - Email: Change `admin@se-prediction.com` to your university email (e.g., `it.admin@university.edu`)
     - Password hash: Replace the long hash with the one generated in step 1
     - Name: Change `Admin User` to appropriate name (e.g., `IT Administrator`)

Example:
```sql
-- BEFORE (default):
INSERT INTO users (name, email, password, role) 
VALUES ('Admin User', 'admin@se-prediction.com', 'scrypt:32768:8:1$...', 'admin');

-- AFTER (customized):
INSERT INTO users (name, email, password, role) 
VALUES ('IT Administrator', 'it.admin@university.edu', 'YOUR_GENERATED_HASH_HERE', 'admin');
```

3. **Create database and import schema:**

```bash
mysql -u root -p
```

```sql
CREATE DATABASE se_prediction_db;
USE se_prediction_db;
SOURCE database_schema.sql;
EXIT;
```

#### Option B: Use Default Admin, Change Later

1. **Import database with default admin:**

```bash
mysql -u root -p
```

```sql
CREATE DATABASE se_prediction_db;
USE se_prediction_db;
SOURCE database_schema.sql;
EXIT;
```

Default credentials:
- Email: `admin@se-prediction.com`
- Password: `admin123`

2. **Change admin credentials using the provided script:**

```bash
source venv/bin/activate
python change_admin.py
```

Follow the interactive prompts to set:
- Admin name
- Admin email (use university email)
- Admin password (choose a strong password)

### Step 4: Configure Environment Variables

1. **Create `.env` file** (if not exists):

```bash
cp .env.example .env  # If example exists
# OR create new .env file
```

2. **Edit `.env` file:**

```env
# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=se_prediction_db
DB_PORT=3306

# Flask Configuration
SECRET_KEY=your-secret-key-here-change-this-in-production
```

**Important:** Change `SECRET_KEY` to a random string for security:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### Step 5: Test the Application

```bash
source venv/bin/activate
python app.py
```

Visit: `http://localhost:5002`

Test login with admin credentials.

### Step 6: Set Up as System Service (Production)

For production deployment, set up the app to run as a system service:

**Create systemd service file** (Linux):

```bash
sudo nano /etc/systemd/system/se-prediction.service
```

```ini
[Unit]
Description=SE Enrollment Prediction System
After=network.target mysql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/SE-Prediction
Environment="PATH=/path/to/SE-Prediction/venv/bin"
ExecStart=/path/to/SE-Prediction/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable se-prediction
sudo systemctl start se-prediction
sudo systemctl status se-prediction
```

---

## 🔒 Security Recommendations

### 1. Change Default Admin Credentials
✅ Use university email domain (e.g., @university.edu)
✅ Use strong password (minimum 12 characters)
✅ Store credentials securely (university password manager)

### 2. Secure Database
✅ Use strong MySQL root password
✅ Create dedicated MySQL user for the application (don't use root)
✅ Set up regular backups

### 3. Configure Firewall
✅ Restrict access to port 5002 (or use nginx/apache as reverse proxy)
✅ Only allow access from university network

### 4. Enable HTTPS
✅ Use SSL certificate (Let's Encrypt or university certificate)
✅ Configure nginx/apache as reverse proxy with HTTPS

---

## 👥 User Management

### Admin Responsibilities:
1. **Approve new user registrations:**
   - Users register on the website
   - Admin reviews and approves from the Admin Dashboard
   - Only approved users can login and use the system

2. **Manage users:**
   - View all registered users
   - Accept or delete user accounts
   - Monitor system usage

### Adding Additional Admins (If Needed):

```bash
mysql -u root -p se_prediction_db
```

```sql
-- Generate password hash first using Python
INSERT INTO users (name, email, password, role, status, created_at) 
VALUES ('Second Admin', 'admin2@university.edu', 'GENERATED_HASH_HERE', 'admin', 'Active', NOW());
```

---

## 📊 Database Backup

Set up automatic daily backups:

```bash
#!/bin/bash
# backup_se_prediction.sh

BACKUP_DIR="/var/backups/se_prediction"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

mysqldump -u root -p se_prediction_db > $BACKUP_DIR/se_prediction_$DATE.sql

# Keep only last 30 days of backups
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
```

Add to crontab:
```bash
crontab -e
# Add line:
0 2 * * * /path/to/backup_se_prediction.sh
```

---

## 🆘 Troubleshooting

### Cannot connect to MySQL:
```bash
# Check MySQL is running
sudo systemctl status mysql

# Check connection
mysql -u root -p -e "SHOW DATABASES;"
```

### Port 5002 already in use:
```bash
# Find process using port 5002
lsof -ti:5002

# Kill process
kill -9 $(lsof -ti:5002)
```

### Forgot admin password:
```bash
# Use the change_admin.py script
source venv/bin/activate
python change_admin.py
```

---

## 📞 Support

For technical issues or questions, contact:
- Developer: Chan Nyein Moe (channyeinmoe2121@gmail.com)
- GitHub: https://github.com/Chan-Nyein21/SE-Prediction

---

## 📝 Version History

- **v1.0** (2025-11-05): Initial release
  - User registration with admin approval
  - Admin dashboard for user management
  - Role-based access control (admin/user)
  - Session management with 30-day expiry
