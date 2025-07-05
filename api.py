from flask import Blueprint, request, jsonify
import uuid
import json
import os

api_bp = Blueprint('api', __name__)

# File paths for persistent storage
USERS_FILE = 'users.json'
SESSIONS_FILE = 'sessions.json'

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    # Default users if file doesn't exist
    return {
        'alice': 'password1',
        'bob': 'password2'
    }

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_sessions():
    """Load sessions from JSON file"""
    if os.path.exists(SESSIONS_FILE):
        try:
            with open(SESSIONS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    return {}

def save_sessions(sessions):
    """Save sessions to JSON file"""
    with open(SESSIONS_FILE, 'w') as f:
        json.dump(sessions, f, indent=2)

# Initialize data
USERS = load_users()
SESSIONS = load_sessions()

@api_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    if username in USERS:
        return jsonify({'error': 'Username already exists'}), 409
    
    USERS[username] = password
    save_users(USERS)  # Save to file
    return jsonify({'message': 'User created successfully'}), 201

@api_bp.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username in USERS and USERS[username] == password:
        token = str(uuid.uuid4())
        SESSIONS[token] = username
        save_sessions(SESSIONS)  # Save to file
        return jsonify({'token': token}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@api_bp.route('/signout', methods=['POST'])
def signout():
    auth = request.headers.get('Authorization', '')
    if auth.startswith('Bearer '):
        token = auth.split(' ', 1)[1]
        if token in SESSIONS:
            SESSIONS.pop(token)
            save_sessions(SESSIONS)  # Save to file
            return jsonify({'message': 'Signed out'}), 200
    return jsonify({'error': 'Invalid token'}), 401 