# tasks.py
from datetime import datetime, timedelta
from app import db
from app.models import User, AdRequest
from flask_mail import Message
from app import mail
from influencer_app.app import celery_utils

@celery_utils.task
def send_daily_reminders():
    now = datetime.utcnow()
    one_day_ago = now - timedelta(days=1)
    
    influencers = User.query.filter_by(role='influencer').all()
    for influencer in influencers:
        if influencer.last_seen < one_day_ago:
            pending_requests = AdRequest.query.filter_by(influencer_id=influencer.id, status='pending').all()
            if pending_requests:
                msg = Message(
                    'Daily Reminder',
                    sender='noreply@showbiz.com',
                    recipients=[influencer.email]
                )
                msg.body = 'You have pending ad requests. Please check your account and take the necessary actions.'
                mail.send(msg)

@celery_utils.task
def send_monthly_reports():
    sponsors = User.query.filter_by(role='sponsor').all()
    for sponsor in sponsors:
        campaigns = sponsor.campaigns  # Assuming you have a relationship set up in your models
        if campaigns:
            msg = Message(
                'Monthly Activity Report',
                sender='noreply@showbiz.com',
                recipients=[sponsor.email]
            )
            msg.body = 'Here is your monthly activity report.'  # Generate a detailed report here
            mail.send(msg)
