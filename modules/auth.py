import jwt
import datetime
from functools import wraps
from flask import request, jsonify
import hashlib
import json
import os

# Simple user database (in production, use a real database)
USERS_FILE = 'data/users.json'

def init_users_file():
    """Initialize users file if it doesn't exist"""
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump({}, f)

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def save_user(email, full_name, password):
    """Save new user to database"""
    init_users_file()
    
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    
    if email in users:
        return False, "User already exists"
    
    users[email] = {
        'full_name': full_name,
        'password': hash_password(password),
        'created_at': datetime.datetime.now().isoformat(),
        'profile_photo': 'default-avatar.png'
    }
    
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)
    
    return True, "User created successfully"

def verify_user(email, password):
    """Verify user credentials"""
    init_users_file()
    
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    
    if email not in users:
        return False, None
    
    if users[email]['password'] == hash_password(password):
        return True, users[email]
    
    return False, None

def get_user(email):
    """Get user information"""
    init_users_file()
    
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    
    return users.get(email)

def update_user_profile(email, updates):
    """Update user profile"""
    init_users_file()
    
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    
    if email in users:
        users[email].update(updates)
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)
        return True
    
    return False

def generate_token(email, secret_key):
    """Generate JWT token"""
    payload = {
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')

def verify_token(token, secret_key):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return True, payload['email']
    except jwt.ExpiredSignatureError:
        return False, "Token expired"
    except jwt.InvalidTokenError:
        return False, "Invalid token"

def token_required(f):
    """Decorator to protect routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'status': 'error', 'message': 'Token missing'}), 401
        
        try:
            token = token.split(" ")[1] if " " in token else token
            from flask import current_app
            valid, email = verify_token(token, current_app.config['SECRET_KEY'])
            
            if not valid:
                return jsonify({'status': 'error', 'message': email}), 401
            
            request.user_email = email
        except Exception as e:
            return jsonify({'status': 'error', 'message': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated