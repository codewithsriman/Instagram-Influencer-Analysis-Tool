import os
from dotenv import load_dotenv

load_dotenv()

# Flask Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Database Configuration
DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'csv')  # 'mysql', 'mongodb', or 'csv'

# MySQL Configuration
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
MYSQL_DB = os.getenv('MYSQL_DB', 'instagram_analytics')

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
MONGODB_DB = os.getenv('MONGODB_DB', 'instagram_analytics')

# Instagram API Configuration
INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN', '')
INSTAGRAM_CLIENT_ID = os.getenv('INSTAGRAM_CLIENT_ID', '')
INSTAGRAM_CLIENT_SECRET = os.getenv('INSTAGRAM_CLIENT_SECRET', '')

# Data Configuration
SAMPLE_DATA_PATH = os.getenv('SAMPLE_DATA_PATH', 'data/sample_data.csv')

# Analytics Configuration
ENGAGEMENT_RATE_THRESHOLD = float(os.getenv('ENGAGEMENT_RATE_THRESHOLD', '3.0'))
CREDIBILITY_THRESHOLD = float(os.getenv('CREDIBILITY_THRESHOLD', '0.7'))
ANOMALY_CONTAMINATION = float(os.getenv('ANOMALY_CONTAMINATION', '0.1'))