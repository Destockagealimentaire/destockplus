import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'votre-cle-secrete-tres-securisee'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///destockage.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuration Stripe
    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY') or 'pk_test_votre_cle'
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY') or 'sk_test_votre_cle'
    
    # Configuration Telegram
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN') or 'votre_token_telegram'
    TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID') or 'votre_chat_id'
    
    # Configuration email (pour confirmations)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')