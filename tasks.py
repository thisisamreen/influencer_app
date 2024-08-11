from datetime import datetime, timedelta
from app.models import *
from flask_mail import Message
from app import mail
from flask import render_template_string,make_response
import random
from io import StringIO
import csv

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



def send_reminder_email(influencer):
    msg = Message('Reminder: Pending Ad Requests', 
                  recipients=[influencer.user.email])
    msg.body = f"Hi {influencer.name},\n\nYou have pending ad requests that need your attention. \nPlease visit the platform to review and take action.\n\nBest regards,\nAdmin"
    mail.send(msg)
    print(f"EMAIL sent!")
    print(f"msg : \n{msg}")



def generate_monthly_report(sponsor):
    campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id).all()

    report_data = []
    for campaign in campaigns:
        num_ads = AdRequest.query.filter_by(campaign_id=campaign.id).count()
        sales_growth = simulate_sales_growth(campaign)  # Replace this with actual logic if available
        budget_used = round(campaign.budget - calculate_remaining_budget(campaign),2)
        
        report_data.append({
            "name": campaign.name,
            "description": campaign.description,
            "num_ads": num_ads,
            "sales_growth": sales_growth,
            "budget_used": budget_used,
            "budget_remaining": round(campaign.budget - budget_used,2)
        })
    
    html_report = render_template_string("""
    <html>
        <body>
            <h1>Monthly Activity Report for {{ sponsor.company_name }}</h1>
            <p>Date: {{ date.strftime('%Y-%m-%d') }}</p>
            {% for campaign in report_data %}
                <h2>{{ campaign.name }}</h2>
                <p>{{ campaign.description }}</p>
                <p>Number of Ads: {{ campaign.num_ads }}</p>
                <p>Growth in Sales: {{ campaign.sales_growth }}%</p>
                <p>Budget Used: ₹{{ campaign.budget_used }}</p>
                <p>Remaining Budget: ₹{{ campaign.budget_remaining }}</p>
            {% endfor %}
        </body>
    </html>
    """, sponsor=sponsor, date=datetime.utcnow(), report_data=report_data)

    return html_report

def simulate_sales_growth(campaign):
    return round(random.uniform(5, 20), 2)

def calculate_remaining_budget(campaign):
    return random.uniform(1000, campaign.budget)




def export_campaigns(sponsor_id):
    sponsor = User.query.get(sponsor_id)
    print(f"sponsor : {sponsor}")
    if not sponsor:
        return None
    
    campaigns = sponsor.campaigns

    # Create a CSV in memory
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Campaign Name', 'Description', 'Start Date', 'End Date', 'Budget', 'Visibility', 'Goals'])

    for campaign in campaigns:
        writer.writerow([
            campaign.name,
            campaign.description,
            campaign.start_date,
            campaign.end_date,
            round(campaign.budget, 2),
            campaign.visibility,
            campaign.goals
        ])

    output.seek(0)
    csv_content = output.getvalue()
    output.close()

    # Send the CSV file as an email attachment
    # msg = Message(
    #     subject=f"Campaigns CSV Export - {sponsor.company_name}",
    #     recipients=[sponsor.email],
    #     body="Please find the attached CSV file containing the details of your campaigns.",
    # )
    # msg.attach(f"campaigns_{sponsor_id}.csv", "text/csv", csv_content)

    # mail.send(msg)
    # print(f"CSV export sent to {sponsor.email}")
    # Create a Flask response object to download the CSV
    response = make_response(csv_content)
    print(f"response : {response}")
    response.headers["Content-Disposition"] = f"attachment; filename=campaigns_{sponsor_id}.csv"
    response.headers["Content-Type"] = "text/csv"
    return response

