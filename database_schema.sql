-- SE Prediction Database Schema
-- Create database
CREATE DATABASE IF NOT EXISTS se_prediction_db;
USE se_prediction_db;

-- Users table (for both students and admins)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Student applications table
CREATE TABLE IF NOT EXISTS applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    
    -- Personal Information
    full_name VARCHAR(255) NOT NULL,
    date_of_birth DATE,
    gender ENUM('Male', 'Female', 'Other'),
    phone VARCHAR(20),
    address TEXT,
    
    -- Academic Information
    high_school_name VARCHAR(255),
    high_school_grade DECIMAL(4,2),
    math_score DECIMAL(5,2),
    english_score DECIMAL(5,2),
    science_score DECIMAL(5,2),
    
    -- Additional Information
    extracurricular_activities TEXT,
    programming_experience ENUM('None', 'Basic', 'Intermediate', 'Advanced') DEFAULT 'None',
    why_software_engineering TEXT,
    
    -- Prediction Results
    prediction_result ENUM('Likely to Enroll', 'Unlikely to Enroll', 'Pending') DEFAULT 'Pending',
    prediction_probability DECIMAL(5,2),
    prediction_date TIMESTAMP NULL,
    
    -- Status
    application_status ENUM('Draft', 'Submitted', 'Under Review', 'Completed') DEFAULT 'Draft',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Admin activities log
CREATE TABLE IF NOT EXISTS admin_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT NOT NULL,
    action VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Insert default admin user (password: admin123)
INSERT INTO users (name, email, password, role) 
VALUES ('Admin User', 'admin@se-prediction.com', 'scrypt:32768:8:1$nqsQlHvvh4xgTDGG$e0e7c3b3c3a8c9b4e8f6d5a2c1b0a9e8d7c6b5a4f3e2d1c0b9a8e7f6d5c4b3a2e1d0c9b8a7e6f5d4c3b2a1e0', 'admin')
ON DUPLICATE KEY UPDATE email=email;

-- Insert sample user (password: user123)
INSERT INTO users (name, email, password, role) 
VALUES ('Test User', 'user@example.com', 'scrypt:32768:8:1$nqsQlHvvh4xgTDGG$a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6', 'user')
ON DUPLICATE KEY UPDATE email=email;
