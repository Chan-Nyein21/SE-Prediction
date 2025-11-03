# SE Prediction - Software Engineering Enrollment Prediction System

A machine learning-powered web application to predict undergraduate registration after admission applications for Software Engineering majors.

## 🚀 Features

### User Role
- Register and login with account approval system
- Upload student data for enrollment predictions
- View prediction results with probability scores
- Access analytics dashboard with model performance metrics

### Admin Role
- **Dashboard**: Manage user registrations (Accept/Delete pending users)
- **Overview**: View enrollment statistics and model accuracy
- **Predict**: Upload data files for batch predictions
- **Results**: Review prediction results for all students
- **Analytics**: Monitor model performance metrics

### Key Highlights
- 30-day persistent sessions with auto-refresh
- Role-based access control (User/Admin)
- File-based storage for demo mode
- Responsive design with Bootstrap 5
- Clean, modern UI with custom color scheme

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, Bootstrap 5.3.0, Bootstrap Icons
- **Backend**: Flask 3.1.2, Werkzeug 3.1.3
- **Database**: MySQL (with demo mode using JSON file storage)
- **ML**: Scikit-learn (to be integrated)
- **Fonts**: Google Fonts (Inter)

## 🎨 Design

**Color Palette:**
- Primary Green: `#3AAA35`
- Primary Blue: `#2B57A5`
- Background: `#E4E8F0`
- Text: `#30693A`
- Active: `#F4B400`

## 📋 Prerequisites

- Python 3.8+
- MySQL 8.0+ (optional - demo mode available)
- pip (Python package manager)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd "SE Prediction"
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run in Demo Mode (No Database Required)**
   ```bash
   python app_demo.py
   ```
   
   Server will start at: `http://localhost:5001`

5. **Or Set up with MySQL** (Optional)
   ```bash
   mysql -u root -p < database_schema.sql
   cp .env.example .env
   # Edit .env file with your MySQL credentials
   python app.py
   ```

## 👥 Demo Credentials

**Admin Account:**
- Email: `admin@gmail.com`
- Password: `admin`

**Test User Account:**
- Email: `user@example.com`
- Password: `user123`

**Note**: New user registrations require admin approval before login access is granted.

## 📁 Project Structure

```
SE Prediction/
├── app_demo.py            # Demo Flask app (file-based storage)
├── app.py                 # Production Flask app (MySQL)
├── requirements.txt       # Python dependencies
├── database_schema.sql    # Database setup script
├── .env.example          # Environment variables template
├── demo_users.json       # Demo user data storage
├── static/
│   ├── css/
│   │   ├── welcome.css       # Landing page styles
│   │   ├── auth.css          # Login/Register styles
│   │   ├── dashboard.css     # Shared dashboard styles
│   │   ├── predict.css       # Prediction page styles
│   │   ├── results.css       # Results table styles
│   │   └── admin-dashboard.css  # User management styles
│   ├── js/
│   │   ├── auth.js           # Password toggle
│   │   ├── dashboard.js      # Logout modal
│   │   ├── predict.js        # File upload handling
│   │   └── admin-dashboard.js   # User actions (Accept/Delete)
│   └── images/
│       └── SE_Logo-removebg-preview.png
└── templates/
    ├── welcome.html       # Landing page
    ├── login.html         # Login page
    ├── register.html      # Registration page
    ├── user/              # User role pages
    │   ├── dashboard.html    # User overview (stats)
    │   ├── predict.html      # Upload predictions
    │   ├── results.html      # View results
    │   └── analytics.html    # Model metrics
    └── admin/             # Admin role pages
        ├── dashboard.html    # User management
        ├── overview.html     # Stats overview
        ├── predict.html      # Upload predictions
        ├── results.html      # View all results
        └── analytics.html    # Model metrics
```

## 🔐 Security Features

- Fixed secret key for persistent sessions across restarts
- 30-day session lifetime with automatic refresh
- Password hashing with Werkzeug security
- Role-based access control (prevents users from accessing admin pages)
- HTTPONLY and Signed session cookies
- User approval workflow (pending → active)

## 📊 Sample Data

**Dashboard Stats:**
- Total Applicants: 800
- Predicted Enrollments: 120
- Model Accuracy: 95.4%

**Analytics Metrics:**
- Overall Accuracy: 92.5%
- Precision: 91.8%
- Recall: 93.2%

## 🚀 Running in Production

For production deployment:

1. Use `app.py` instead of `app_demo.py`
2. Set up MySQL database
3. Configure proper environment variables in `.env`
4. Change `SECRET_KEY` to a secure random string
5. Enable HTTPS and set `SESSION_COOKIE_SECURE = True`
6. Use a production WSGI server (Gunicorn, uWSGI)
7. Disable debug mode

## 🐛 Troubleshooting

**Port already in use:**
```bash
lsof -ti:5001 | xargs kill -9
```

**Session issues:**
- Clear browser cookies
- Check `demo_users.json` exists and is readable
- Verify `SECRET_KEY` hasn't changed

**Access denied:**
- Users can only access `/user/*` pages
- Admins can only access `/admin/*` pages
- This is by design (role-based access control)

## 📝 License

This project is created for educational purposes.

## 👨‍💻 Development

Developed for Software Engineering undergraduate enrollment prediction at Mila Tech Unsiing University.

**Version**: 1.0.0  
**Last Updated**: November 2025
