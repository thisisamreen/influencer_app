from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    company_name = db.Column(db.String(100))  # Only relevant for sponsors
    industry = db.Column(db.String(100))  # Only relevant for sponsors
    budget = db.Column(db.Float)  # Only relevant for sponsors
    # Backreference for campaigns created by the sponsor
    campaigns = db.relationship('Campaign', backref='sponsor', lazy=True)
    # ad_requests = db.relationship('AdRequest', back_populates='influencer', lazy=True)
    ad_requests = db.relationship('AdRequest', foreign_keys='AdRequest.influencer_id', back_populates='influencer', lazy=True)
    profile = db.relationship('InfluencerProfile', uselist=False, back_populates='user')
    is_flagged = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    visibility = db.Column(db.String(10), nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    goals = db.Column(db.Text, nullable=False)
    # Backreference for ad requests related to the campaign
    # ad_requests = db.relationship('AdRequest', backref='campaign', lazy=True)
    ad_requests = db.relationship('AdRequest', foreign_keys='AdRequest.campaign_id', back_populates='campaign', lazy=True)
    is_flagged = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return f"Campaign('{self.name}', '{self.category}', '{self.start_date}', '{self.end_date}')"

class AdRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    messages = db.Column(db.Text, )
    requirements = db.Column(db.Text, )
    payment_amount = db.Column(db.Float, )
    status = db.Column(db.String(10),default='Pending')
    counter_amount = db.Column(db.Float) # Influencer Counter Amount
    proposed_amount = db.Column(db.Float, ) # Sponosr counter amount
    negotiation_status = db.Column(db.String(20),  default='Open')  # Open, Closed
    campaign = db.relationship('Campaign', back_populates='ad_requests',lazy=True)
    influencer = db.relationship('User', back_populates='ad_requests',lazy=True)
    def __repr__(self):
        return f"AdRequest('{self.id}', '{self.status}', '{self.payment_amount}')"

class InfluencerProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100),)
    niche = db.Column(db.String(100), )
    reach = db.Column(db.Integer,)
    # Backreference for the user
    user = db.relationship('User', back_populates='profile')

    def __repr__(self):
        return f"InfluencerProfile('{self.name}', '{self.category}', '{self.niche}', '{self.reach}')"
