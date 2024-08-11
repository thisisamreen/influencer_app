from app import create_app, db
from app.models import User, InfluencerProfile, Campaign, AdRequest
from flask_bcrypt import Bcrypt
import datetime

app = create_app()
bcrypt = Bcrypt(app)

with app.app_context():
    # Drop all tables and recreate them
    db.drop_all()
    db.create_all()

    # Create admin user
    admin = User(
        username='admin',
        email='admin@example.com',
        password=bcrypt.generate_password_hash('admin').decode('utf-8'),
        role='admin'
    )
    db.session.add(admin)

    # Create sponsors
    sponsor1 = User(
        username='sponsor1',
        email='sponsor1@example.com',
        password=bcrypt.generate_password_hash('sponsor1').decode('utf-8'),
        role='sponsor',
        company_name='Sponsor Company 1',
        industry='Tech',
        budget=10000.0
    )

    sponsor2 = User(
        username='sponsor2',
        email='sponsor2@example.com',
        password=bcrypt.generate_password_hash('sponsor2').decode('utf-8'),
        role='sponsor',
        company_name='Sponsor Company 2',
        industry='Health',
        budget=15000.0
    )

    db.session.add(sponsor1)
    db.session.add(sponsor2)

    # Create influencers
    influencer1 = User(
        username='influencer1',
        email='influencer1@example.com',
        password=bcrypt.generate_password_hash('influencer1').decode('utf-8'),
        role='influencer'
    )
    influencer1_profile = InfluencerProfile(
        user=influencer1,
        name='Influencer One',
        category='Fitness',
        niche='Yoga',
        reach=10000,
        last_visited = datetime.date(2024,8,1)
    )

    influencer2 = User(
        username='influencer2',
        email='influencer2@example.com',
        password=bcrypt.generate_password_hash('influencer2').decode('utf-8'),
        role='influencer',
        
    )
    influencer2_profile = InfluencerProfile(
        user=influencer2,
        name='Influencer Two',
        category='Tech',
        niche='Gadgets',
        reach=20000,
        last_visited = datetime.date(2024,8,3)
    )

    influencer3 = User(
        username='influencer3',
        email='influencer3@example.com',
        password=bcrypt.generate_password_hash('influencer3').decode('utf-8'),
        role='influencer'
    )
    influencer3_profile = InfluencerProfile(
        user=influencer3,
        name='Influencer Three',
        category='Food',
        niche='Vegan Recipes',
        reach=15000,
        last_visited = datetime.date(2024,8,11)
    )

    db.session.add(influencer1)
    db.session.add(influencer1_profile)
    db.session.add(influencer2)
    db.session.add(influencer2_profile)
    db.session.add(influencer3)
    db.session.add(influencer3_profile)

    # Create campaigns
    campaign1 = Campaign(
        name='Campaign One',
        description='This is campaign one',
        category='Tech',
        start_date=datetime.date(2024, 1, 1),
        end_date=datetime.date(2024, 12, 31),
        budget=5000.0,
        visibility='public',
        sponsor=sponsor1,
        goals='Increase brand awareness'
    )

    campaign2 = Campaign(
        name='Campaign Two',
        description='This is campaign two',
        category='Health',
        start_date=datetime.date(2024, 2, 1),
        end_date=datetime.date(2024, 11, 30),
        budget=8000.0,
        visibility='public',
        sponsor=sponsor2,
        goals='Boost sales'
    )

    db.session.add(campaign1)
    db.session.add(campaign2)

    # Create ad requests
    ad_request1 = AdRequest(
        campaign=campaign1,
        influencer=influencer1,
        messages='Please promote our new tech gadget.',
        requirements='Minimum 3 posts',
        payment_amount=1000.0,
        status='Pending'
    )

    ad_request2 = AdRequest(
        campaign=campaign2,
        influencer=influencer2,
        messages='Promote our new health supplement.',
        requirements='Minimum 2 posts',
        payment_amount=1500.0,
        status='Pending'
    )

    db.session.add(ad_request1)
    db.session.add(ad_request2)

    # Commit all changes to the database
    db.session.commit()

    print("Database initialized with users, profiles, campaigns, and ad requests.")
