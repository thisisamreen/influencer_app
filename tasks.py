from datetime import datetime, timedelta
# from celery import Celery, Task
from app.models import InfluencerProfile, AdRequest
# from app import celery  




def get_influencers_with_pending_requests():
    visit_threshold = datetime.utcnow() - timedelta(days=1)
    
    influencers_to_remind = []
    influencers = InfluencerProfile.query.all()
    # influencers = InfluencerProfile.query.filter(InfluencerProfile.last_visited < visit_threshold)
    
    for influencer in influencers:
        print(f"{influencer.name}  last_visited: {influencer.last_visited}")
        print(f"visit_threshold : {visit_threshold}")
        if influencer.last_visited < visit_threshold:
            # pending_requests = AdRequest.query.filter_by(influencer_id=influencer.id).count()  #status='Pending'
            pending_requests = AdRequest.query.filter_by(influencer_id=influencer.user_id, status='Pending').count()

            print(f"request pending for {influencer}  : {pending_requests}")
            if pending_requests > 0:
                print(f"Reminder list appended with {influencer.name}")
                influencers_to_remind.append(influencer)
    print(f"influencers_to_remind : {influencers_to_remind}")
    return influencers_to_remind


def send_reminder(influencer):
    # print(f"Sending mail to {influencer}")
    print(f"Sending mail to {influencer.name}")

