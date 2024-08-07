# from app import db, create_app,bcrypt
# from app.models import User, Campaign, AdRequest
# from flask_bcrypt import Bcrypt
# from datetime import date

# app = create_app()
# app.app_context().push()

# bcrypt = Bcrypt(app)

# # Drop all tables
# db.drop_all()

# # Create all tables
# db.create_all()

# # Create admin user
# admin_password = bcrypt.generate_password_hash('admin').decode('utf-8')
# admin = User(username='admin', email='admin@example.com', password=admin_password, role='admin')
# db.session.add(admin)

# # Create a sponsor user
# sponsor_password = bcrypt.generate_password_hash('sponsor').decode('utf-8')
# sponsor = User(username='sponsor_user', email='sponsor@example.com', password=sponsor_password, role='sponsor', company_name='Tech Corp', industry='Technology', budget=10000)
# db.session.add(sponsor)

# # Create campaigns
# campaign1 = Campaign(
#     name='Tech Campaign',
#     description='A campaign to promote tech products',
#     category='Tech',
#     start_date=date(2024, 8, 4),
#     end_date=date(2024, 12, 31),
#     budget=5000.0,
#     visibility='public',
#     sponsor=sponsor,
#     goals='Promote our latest tech products'
# )

# campaign2 = Campaign(
#     name='Gaming Campaign',
#     description='A campaign to promote gaming products',
#     category='Gaming',
#     start_date=date(2024, 8, 4),
#     end_date=date(2024, 12, 31),
#     budget=7000.0,
#     visibility='public',
#     sponsor=sponsor,
#     goals='Promote our latest gaming products'
# )

# db.session.add(campaign1)
# db.session.add(campaign2)

# # Create an influencer user
# influencer_password = bcrypt.generate_password_hash('influencer').decode('utf-8')
# influencer = User(username='influencer_user', email='influencer@example.com', password=influencer_password, role='influencer')
# db.session.add(influencer)

# # Create ad requests
# ad_request1 = AdRequest(
#     campaign=campaign1.id,
#     influencer=influencer.id,
#     messages='Please promote our product in your next video',
#     requirements='Mention our product name and show its features',
#     payment_amount=1000.0,
#     status='Pending'
# )

# ad_request2 = AdRequest(
#     campaign=campaign2.id,
#     influencer=influencer,
#     messages='Please promote our gaming product',
#     requirements='Show gameplay and mention features',
#     payment_amount=1500.0,
#     status='Pending'
# )

# db.session.add(ad_request1)
# db.session.add(ad_request2)

# # Commit the changes
# db.session.commit()


from app import db, create_app, bcrypt
from flask_bcrypt import Bcrypt
from app.models import User, Campaign, AdRequest
from datetime import date

app = create_app()
app.app_context().push()

bcrypt = Bcrypt(app)

# Drop all tables
db.drop_all()

# Create all tables
db.create_all()

# Create admin user
admin_password = bcrypt.generate_password_hash('admin').decode('utf-8')
admin = User(username='admin', email='admin@example.com', password=admin_password, role='admin')
db.session.add(admin)

# Create a sponsor user
sponsor_password = bcrypt.generate_password_hash('sponsor').decode('utf-8')
sponsor = User(username='sponsor_user', email='sponsor@example.com', password=sponsor_password, role='sponsor', company_name='Tech Corp', industry='Technology', budget=10000)
db.session.add(sponsor)

# Create an influencer user
influencer_password = bcrypt.generate_password_hash('influencer').decode('utf-8')
influencer = User(username='influencer_user', email='influencer@example.com', password=influencer_password, role='influencer')
db.session.add(influencer)

# Commit users to the database so they get their IDs
db.session.commit()

# Create campaigns
campaign1 = Campaign(
    name='Tech Campaign',
    description='A campaign to promote tech products',
    category='Tech',
    start_date=date(2024, 8, 4),
    end_date=date(2024, 12, 31),
    budget=5000.0,
    visibility='public',
    sponsor_id=sponsor.id,
    goals='Promote our latest tech products'
)

campaign2 = Campaign(
    name='Gaming Campaign',
    description='A campaign to promote gaming products',
    category='Gaming',
    start_date=date(2024, 8, 4),
    end_date=date(2024, 12, 31),
    budget=7000.0,
    visibility='public',
    sponsor_id=sponsor.id,
    goals='Promote our latest gaming products'
)

db.session.add(campaign1)
db.session.add(campaign2)

# Commit campaigns to the database so they get their IDs
db.session.commit()

# Create ad requests
ad_request1 = AdRequest(
    campaign_id=campaign1.id,
    influencer_id=influencer.id,
    messages='Please promote our product in your next video',
    requirements='Mention our product name and show its features',
    payment_amount=1000.0,
    status='Open'
)

ad_request2 = AdRequest(
    campaign_id=campaign2.id,
    influencer_id=influencer.id,
    messages='Please promote our gaming product',
    requirements='Show gameplay and mention features',
    payment_amount=1500.0,
    status='Open'
)

db.session.add(ad_request1)
db.session.add(ad_request2)

# Commit the ad requests
db.session.commit()
