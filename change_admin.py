#!/usr/bin/env python3
"""
Change Admin Credentials Script
This script allows you to safely change the admin username (email) and password
in the SE Prediction database.
"""

from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import MySQLdb
import os
import sys

# Load environment variables from .env file
load_dotenv()

def main():
    print("=" * 60)
    print("🔐 SE Prediction - Change Admin Credentials")
    print("=" * 60)
    print()
    
    # Get database credentials from .env
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'se_prediction_db')
    }
    
    try:
        # Connect to database
        print("📡 Connecting to database...")
        conn = MySQLdb.connect(
            host=db_config['host'],
            user=db_config['user'],
            passwd=db_config['password'],
            db=db_config['database']
        )
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        
        # Show current admin info
        cursor.execute("SELECT name, email FROM users WHERE role = 'admin'")
        current_admin = cursor.fetchone()
        
        if current_admin:
            print(f"✅ Connected successfully!")
            print()
            print("Current admin information:")
            print(f"  Name:  {current_admin['name']}")
            print(f"  Email: {current_admin['email']}")
            print()
        else:
            print("⚠️  No admin user found in database!")
            return
        
        # Ask if user wants to proceed
        proceed = input("Do you want to change admin credentials? (yes/no): ").strip().lower()
        if proceed not in ['yes', 'y']:
            print("❌ Operation cancelled.")
            return
        
        print()
        print("=" * 60)
        print("Enter new admin credentials:")
        print("=" * 60)
        
        # Get new credentials from user
        new_name = input("Enter new admin name (press Enter to keep current): ").strip()
        new_email = input("Enter new admin email (press Enter to keep current): ").strip()
        new_password = input("Enter new admin password (press Enter to skip): ").strip()
        
        # Validate inputs
        if not new_name and not new_email and not new_password:
            print("⚠️  No changes were made.")
            return
        
        # Build update query dynamically
        updates = []
        params = []
        
        if new_name:
            updates.append("name = %s")
            params.append(new_name)
        
        if new_email:
            updates.append("email = %s")
            params.append(new_email)
        
        if new_password:
            # Hash the password
            print("\n🔒 Hashing password...")
            hashed_password = generate_password_hash(new_password)
            updates.append("password = %s")
            params.append(hashed_password)
        
        # Execute update
        if updates:
            query = f"UPDATE users SET {', '.join(updates)} WHERE role = 'admin'"
            cursor.execute(query, tuple(params))
            conn.commit()
            
            print()
            print("=" * 60)
            print("✅ Admin credentials updated successfully!")
            print("=" * 60)
            
            # Show new admin info
            cursor.execute("SELECT name, email FROM users WHERE role = 'admin'")
            updated_admin = cursor.fetchone()
            
            print()
            print("New admin information:")
            print(f"  Name:  {updated_admin['name']}")
            print(f"  Email: {updated_admin['email']}")
            if new_password:
                print(f"  Password: (updated - {len(new_password)} characters)")
            print()
            print("🚀 You can now login with these new credentials!")
            print()
        
        # Close connection
        cursor.close()
        conn.close()
        
    except MySQLdb.Error as err:
        print(f"❌ Database error: {err}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
