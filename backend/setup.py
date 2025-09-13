#!/usr/bin/env python
"""
Setup script for Cinemajoo Django Backend
This script helps initialize the Django project
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install Python dependencies"""
    return run_command("pip install -r requirements.txt", "Installing dependencies")

def setup_database():
    """Set up the database"""
    commands = [
        ("python manage.py makemigrations", "Creating database migrations"),
        ("python manage.py migrate", "Applying database migrations"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    return True

def create_superuser():
    """Create a superuser account"""
    print("🔐 Creating superuser account...")
    print("Please enter the following information:")
    
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    
    if not all([username, email, password]):
        print("❌ All fields are required")
        return False
    
    command = f"python manage.py createsuperuser --username {username} --email {email} --password {password}"
    return run_command(command, "Creating superuser")

def main():
    """Main setup function"""
    print("🚀 Welcome to Cinemajoo Django Backend Setup!")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        print("❌ Setup failed at database setup")
        sys.exit(1)
    
    # Ask if user wants to create superuser
    create_super = input("\n🤔 Would you like to create a superuser account? (y/n): ").lower().strip()
    if create_super in ['y', 'yes']:
        if not create_superuser():
            print("⚠️  Superuser creation failed, but you can create one manually later")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start the server: python manage.py runserver")
    print("2. Access admin panel: http://localhost:8000/admin/")
    print("3. API endpoints: http://localhost:8000/api/")
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main()








