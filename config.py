import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_secret_key_change_in_prod'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///loan.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload

    # Ensure upload directory exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # DigiLocker Configuration (Sandbox/Production)
    # Replace with your actual credentials from DigiLocker Partner Portal
    DIGILOCKER_CLIENT_ID = os.environ.get('DIGILOCKER_CLIENT_ID') or 'YOUR_DIGILOCKER_CLIENT_ID' 
    DIGILOCKER_CLIENT_SECRET = os.environ.get('DIGILOCKER_CLIENT_SECRET') or 'YOUR_DIGILOCKER_CLIENT_SECRET'
    DIGILOCKER_REDIRECT_URI = os.environ.get('DIGILOCKER_REDIRECT_URI') or 'http://localhost:5000/auth/digilocker/callback'
    
    # Set to True to test the flow without real DigiLocker credentials
    DIGILOCKER_MOCK_MODE = True # Enabled for testing without keys
    
    # DigiLocker Endpoints (Dev/Sandbox)
    # Updated based on user provided CURL: https://dev-meripehchaan.dl6.in/...
    DIGILOCKER_AUTH_URL = 'https://dev-meripehchaan.dl6.in/public/oauth2/1/authorize'
    DIGILOCKER_TOKEN_URL = 'https://dev-meripehchaan.dl6.in/public/oauth2/1/token'
    DIGILOCKER_USER_URL = 'https://dev-meripehchaan.dl6.in/public/oauth2/1/user'

    # Mail Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None or True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    MAIL_DEFAULT_SENDER = os.environ.get('EMAIL_USER')
