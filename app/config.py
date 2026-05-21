import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///product_intro_ex.db'  # デフォルトはローカル SQLite
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Claude API
    CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')

    # SNS APIs
    NOTE_API_KEY = os.getenv('NOTE_API_KEY')
    TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
    TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
    TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')

    # Affiliate
    AFFILIATE_API_KEY = os.getenv('AFFILIATE_API_KEY')

    # Scheduler
    SCHEDULER_TIMEZONE = os.getenv('SCHEDULER_TIMEZONE', 'Asia/Tokyo')
    POST_TIME = os.getenv('POST_TIME', '09:00')
