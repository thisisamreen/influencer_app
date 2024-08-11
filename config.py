import os

class Config:
    SECRET_KEY = 'my_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'app.db')
    CELERY_BROKER_URL =  "redis://localhost:6379/0"         #os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"              #os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_BEAT_SCHEDULE = {
        'send-daily-reminders': {
            'task': 'app.send_daily_reminder',
            'schedule': 60.0 *3 ,# Run every 24 hours* 60.0 * 24.0, 
            'options': {
                'expires': 60.0*4  # Task expires if not run within 24 hours  * 60.0 * 24.0
            }
        },
    }
    CELERY_TIMEZONE = 'UTC'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('EMAIL_USER')
    # MAIL_PASSWORD = os.environ.get('EMAIL_PASS')