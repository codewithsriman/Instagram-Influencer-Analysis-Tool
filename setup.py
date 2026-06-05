#!/usr/bin/env python3
"""
Instagram Influencer Analytics - Setup Script
Automates the setup process for the application
"""

import os
import sys
import subprocess

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required")
        print("Please upgrade Python and try again")
        return False
    
    print("✅ Python version is compatible")
    return True

def create_directories():
    """Create required directory structure"""
    print_header("Creating Directory Structure")
    
    directories = [
        'data',
        'modules',
        'utils',
        'templates',
        'static/css',
        'static/js',
        'backups'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created: {directory}/")
    
    return True

def create_env_file():
    """Create .env file with default configuration"""
    print_header("Creating Configuration File")
    
    env_content = """# Flask Configuration
SECRET_KEY=dev-secret-key-change-in-production
DEBUG=True

# Database Configuration
DATABASE_TYPE=csv
SAMPLE_DATA_PATH=data/sample_data.csv

# Analytics Configuration
ENGAGEMENT_RATE_THRESHOLD=3.0
CREDIBILITY_THRESHOLD=0.7
ANOMALY_CONTAMINATION=0.1

# Instagram API (Optional - for real data)
INSTAGRAM_ACCESS_TOKEN=
INSTAGRAM_CLIENT_ID=
INSTAGRAM_CLIENT_SECRET=
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file with default configuration")
    else:
        print("ℹ️  .env file already exists (skipping)")
    
    return True

def install_dependencies():
    """Install Python dependencies"""
    print_header("Installing Python Dependencies")
    
    try:
        print("Installing packages from requirements.txt...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ All dependencies installed successfully")
        
        print("\nDownloading TextBlob corpora...")
        subprocess.check_call([sys.executable, '-m', 'textblob.download_corpora'])
        print("✅ TextBlob corpora downloaded")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_init_files():
    """Create __init__.py files for Python packages"""
    print_header("Creating Python Package Files")
    
    # modules/__init__.py
    modules_init = 'modules/__init__.py'
    if not os.path.exists(modules_init):
        with open(modules_init, 'w') as f:
            f.write('"""Instagram Influencer Analytics Modules"""\n')
        print(f"✅ Created {modules_init}")
    
    # utils/__init__.py
    utils_init = 'utils/__init__.py'
    if not os.path.exists(utils_init):
        with open(utils_init, 'w') as f:
            f.write('"""Utility Functions"""\n')
        print(f"✅ Created {utils_init}")
    
    return True

def verify_files():
    """Verify all required files exist"""
    print_header("Verifying File Structure")
    
    required_files = {
        'Core Files': [
            'app.py',
            'config.py',
            'requirements.txt'
        ],
        'Modules': [
            'modules/auth.py',
            'modules/brand_recommendation.py',
            'modules/data_collection.py',
            'modules/data_preprocessing.py',
            'modules/fake_follower_detection.py',
            'modules/metrics_computation.py',
            'modules/sentiment_analysis.py',
            'modules/user_search.py'
        ],
        'Templates': [
            'templates/login.html',
            'templates/signup.html',
            'templates/profile.html',
            'templates/dashboard.html'
        ],
        'Static Files': [
            'static/css/style.css',
            'static/js/auth.js',
            'static/js/dashboard.js',
            'static/js/search.js'
        ],
        'Utils': [
            'utils/helpers.py'
        ]
    }
    
    all_good = True
    for category, files in required_files.items():
        print(f"\n{category}:")
        for file in files:
            if os.path.exists(file):
                print(f"  ✅ {file}")
            else:
                print(f"  ❌ {file} (MISSING)")
                all_good = False
    
    return all_good

def print_next_steps():
    """Print instructions for running the application"""
    print_header("Setup Complete!")
    
    print("""
🎉 Installation successful! 

📋 Next Steps:

1. Start the application:
   python app.py

2. Open your browser:
   http://localhost:5000

3. Create an account:
   Click "Sign Up" and register

4. Start analyzing:
   - Click "Analyze All Influencers"
   - Or search specific usernames
   - View AI brand recommendations

📚 Documentation:
   - README.md - Full documentation
   - QUICKSTART.md - Quick start guide
   - NEW_FEATURES.md - Feature overview

🔧 Configuration:
   - Edit .env for custom settings
   - Modify config.py for advanced options

💡 Tips:
   - Sample data is auto-generated on first run
   - Test with usernames like: fashionista_maya, tech_guru_raj
   - Check data/users.json for created accounts

🚀 Ready to launch!
    """)

def main():
    """Main setup function"""
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   Instagram Influencer Impact Analysis Tool             ║
║   Automated Setup Script                                ║
║   Version 2.0                                           ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Run setup steps
    steps = [
        ("Checking Python version", check_python_version),
        ("Creating directories", create_directories),
        ("Creating configuration", create_env_file),
        ("Installing dependencies", install_dependencies),
        ("Creating package files", create_init_files),
        ("Verifying installation", verify_files)
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Setup failed at: {step_name}")
            print("Please fix the errors and run setup again")
            sys.exit(1)
    
    # Print success message
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)