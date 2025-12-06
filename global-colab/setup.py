#!/usr/bin/env python3
"""
Quick setup script for Global Collaborative Learning Platform
This script helps verify the setup and provides basic checks.
"""

import sys
import pymysql

def check_database():
    """Check if database connection works"""
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='global_colab',
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        print(f"✓ Database connection successful! Found {count} users.")
        return True
    except pymysql.Error as e:
        print(f"✗ Database connection failed: {e}")
        print("\nPlease ensure:")
        print("1. XAMPP MySQL is running")
        print("2. Database 'global_colab' exists")
        print("3. Database schema has been imported")
        return False

def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = ['flask', 'flask_cors', 'pymysql']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is NOT installed")
            missing.append(package)
    
    if missing:
        print(f"\nPlease install missing packages:")
        print(f"pip install {' '.join(missing)}")
        return False
    return True

def main():
    print("=" * 50)
    print("Global Collaborative Learning Platform - Setup Check")
    print("=" * 50)
    print()
    
    print("Checking Python dependencies...")
    deps_ok = check_dependencies()
    print()
    
    if deps_ok:
        print("Checking database connection...")
        db_ok = check_database()
        print()
        
        if db_ok:
            print("=" * 50)
            print("✓ Setup looks good! You can run the application with:")
            print("  python app.py")
            print("=" * 50)
        else:
            print("=" * 50)
            print("✗ Please fix database issues before running the app")
            print("=" * 50)
            sys.exit(1)
    else:
        print("=" * 50)
        print("✗ Please install missing dependencies")
        print("=" * 50)
        sys.exit(1)

if __name__ == '__main__':
    main()

