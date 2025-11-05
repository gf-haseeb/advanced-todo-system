"""Configuration settings for the Flask API backend."""

import os

# Flask Configuration
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = FLASK_ENV == 'development'
HOST = '127.0.0.1'
PORT = 5000

# CORS Configuration
CORS_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:5000',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:5000',
    '*',  # Allow all origins in development
]

# Storage Configuration
STORAGE_PATH = os.path.expanduser('~/.my_todo_lib')
TASKS_FILE = os.path.join(STORAGE_PATH, 'tasks.json')

# API Configuration
API_VERSION = 'v1'
API_PREFIX = f'/api/{API_VERSION}'
