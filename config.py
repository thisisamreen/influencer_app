import os
from dotenv import load_dotenv
from celery.schedules import crontab

load_dotenv()
class Config:
    SECRET_KEY = 'my_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'app.db')
    CELERY_BROKER_URL =  "redis://localhost:6379/0"         #os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"              #os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_BEAT_SCHEDULE = {
        'send-daily-reminders': {
            'task': 'app.send_daily_reminder',
            'schedule': 60.0 *60.0 * 24.0,# Run every 24 hours* 
            'options': {
                'expires': 60.0*60.0 * 24.0,  # Task expires if not run within 24 hours  * 60.0 * 24.0
            }
        },
        'send-monthly-reports': {
            'task': 'app.send_monthly_report',
            'schedule':crontab(day_of_month=1, hour=0, minute=0),    
            'options': {
                'expires': 60.0 * 60.0 * 24.0}, 
            },

    }
    CELERY_TIMEZONE = 'UTC'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.getenv('EMAIL_USER')
    MAIL_PASSWORD = os.getenv('EMAIL_PASS')
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER') 
    print(f"EMAIL  USER= {MAIL_USERNAME}")
    print(f"EMAIL  PASS= {MAIL_PASSWORD}")
    print(f"EMAIL  = {MAIL_DEFAULT_SENDER}")
    print(f"RECIPIENTS MAIL :{os.getenv("RECIPIENTS_EMAIL")}")