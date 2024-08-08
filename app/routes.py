from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.forms import *
from app.models import *
from functools import wraps

main = Blueprint('main', __name__)

# Decorator to restrict access to admins only
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            flash('You do not have access to this page.', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function

def sponsor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'sponsor':
            flash('You do not have access to this page.', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function

def influencer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'influencer':
            flash('You do not have access to this page.', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function

@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html', title='Home')



@main.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            elif user.role == 'admin':
                return redirect(url_for('main.admin_dashboard'))
            elif user.role == 'sponsor':
                return redirect(url_for('main.sponsor_dashboard'))
            elif user.role == 'influencer':
                return redirect(url_for('main.influencer_dashboard'))
            else:
                return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


# Sponsor Dashboard

@main.route("/sponsor/dashboard", methods=['GET', 'POST'])
@login_required
@sponsor_required
def sponsor_dashboard():
    if current_user.role != 'sponsor':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('main.home'))
    form = SponsorProfileForm()
    search_form = SearchForm()
    ad_form = CreateAdRequestForm()
    influencer_search_form = InfluencerSearchForm()
    campaigns = Campaign.query.filter_by(sponsor_id=current_user.id).all()
    ad_requests = AdRequest.query.filter(AdRequest.campaign_id.in_([campaign.id for campaign in campaigns])).all()
    if search_form.submit.data and search_form.validate_on_submit():
        search_query = search_form.search.data
        campaigns = Campaign.query.filter(
            Campaign.sponsor_id == current_user.id,
            Campaign.name.ilike(f'%{search_query}%')
        ).all()
        flash(f'Search results for "{search_query}":', 'info')
    elif influencer_search_form.submit.data and influencer_search_form.validate_on_submit():
        search_query = influencer_search_form.search.data
        influencers = User.query.join(InfluencerProfile).filter(
            User.role == 'influencer',
            db.or_(
                InfluencerProfile.name.ilike(f'%{search_query}%'),
                InfluencerProfile.category.ilike(f'%{search_query}%'),
                InfluencerProfile.niche.ilike(f'%{search_query}%')
            )
        ).all()
        flash(f'Search results for "{search_query}":', 'info')
        return render_template('search_influencers.html', influencers=influencers, search_form=influencer_search_form)

    elif form.submit.data and form.validate_on_submit():
        current_user.company_name = form.company_name.data
        current_user.industry = form.industry.data
        current_user.budget = form.budget.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.sponsor_dashboard'))
    ad_requests = AdRequest.query.join(Campaign).filter(Campaign.sponsor_id == current_user.id).all()
    return render_template('sponsor_dashboard.html', campaigns=campaigns, ad_requests=ad_requests, search_form=search_form, influencer_search_form=influencer_search_form)
    # return render_template('sponsor_dashboard.html', campaigns=campaigns, form=form, search_form=search_form,ad_form=ad_form)

@main.route("/sponsor/profile", methods=['GET', 'POST'])
@login_required
@sponsor_required
def sponsor_profile():
    form = SponsorProfileForm()
    if form.validate_on_submit():
        current_user.company_name = form.company_name.data
        current_user.industry = form.industry.data
        current_user.budget = form.budget.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.sponsor_dashboard'))
    elif request.method == 'GET':
        form.company_name.data = current_user.company_name
        form.industry.data = current_user.industry
        form.budget.data = current_user.budget
    return render_template('sponsor_profile.html', title='Sponsor Profile', form=form)

@main.route("/sponsor/campaigns", methods=['GET'])
@login_required
@sponsor_required
def sponsor_campaigns():
    campaigns = Campaign.query.filter_by(sponsor_id=current_user.id).all()
    return render_template('sponsor_campaigns.html', campaigns=campaigns)


@main.route("/sponsor/campaigns/new", methods=['GET', 'POST'])
@login_required
@sponsor_required
def new_campaign():
    form = CampaignForm()
    if form.validate_on_submit():
        campaign = Campaign(name=form.name.data,
                             description=form.description.data, 
                             category=form.category.data,
                            start_date=form.start_date.data, 
                            end_date=form.end_date.data,
                              budget=form.budget.data,
                            visibility=form.visibility.data, 
                            goals=form.goals.data, 
                            sponsor_id=current_user.id
                            )
        db.session.add(campaign)
        db.session.commit()
        flash('Your campaign has been created!', 'success')
        return redirect(url_for('main.sponsor_dashboard'))
    return render_template('create_campaign.html', title='New Campaign', form=form, legend='New Campaign')

@main.route("/sponsor/campaigns/<int:campaign_id>/update", methods=['GET', 'POST'])
@login_required
@sponsor_required
def update_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.sponsor != current_user:
        flash('You do not have access to this page.', 'danger')
    form = CampaignForm()
    if form.validate_on_submit():
        campaign.name = form.name.data
        campaign.description = form.description.data
        campaign.category = form.category.data
        campaign.start_date = form.start_date.data
        campaign.end_date = form.end_date.data
        campaign.budget = form.budget.data
        campaign.visibility = form.visibility.data
        campaign.goals = form.goals.data
        db.session.commit()
        flash('Your campaign has been updated!', 'success')
        return redirect(url_for('main.sponsor_dashboard'))
    elif request.method == 'GET':
        form.name.data = campaign.name
        form.description.data = campaign.description
        form.category.data = campaign.category
        form.start_date.data = campaign.start_date
        form.end_date.data = campaign.end_date
        form.budget.data = campaign.budget
        form.visibility.data = campaign.visibility
        form.goals.data = campaign.goals
    return render_template('create_campaign.html', title='Update Campaign', form=form, legend='Update Campaign')

@main.route("/sponsor/campaigns/<int:campaign_id>/delete", methods=['POST'])
@login_required
@sponsor_required
def delete_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.sponsor != current_user:
        flash('You do not have access to this page.', 'danger')
    db.session.delete(campaign)
    db.session.commit()
    flash('Your campaign has been deleted!', 'success')
    return redirect(url_for('main.sponsor_dashboard'))


@main.route("/sponsor/ad_request/new", methods=['GET', 'POST'])
@login_required
@sponsor_required
def new_ad_request():
    form = CreateAdRequestForm()
    form.campaign_id.choices = [(campaign.id, campaign.name) for campaign in Campaign.query.filter_by(sponsor_id=current_user.id).all()]
    form.influencer_id.choices = [(user.id, user.username) for user in User.query.filter_by(role='influencer').all()]

    if form.validate_on_submit():
        ad_request = AdRequest(
            campaign_id=form.campaign_id.data,
            influencer_id=form.influencer_id.data,
            messages=form.messages.data,
            requirements=form.requirements.data,
            payment_amount=form.payment_amount.data,
            status='Pending'
        )
        db.session.add(ad_request)
        db.session.commit()
        flash('Your ad request has been created!', 'success')
        return redirect(url_for('main.view_ad_requests'))
    return render_template('create_ad_request.html', title='New Ad Request', form=form, legend='New Ad Request',form_action='main.new_ad_request', ad_request_id=None)

@main.route("/sponsor/ad_request/<int:ad_request_id>/update", methods=['GET', 'POST'])
@login_required
@sponsor_required
def update_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    form = UpdateAdRequestForm()
    form.campaign_id.choices = [(campaign.id, campaign.name) for campaign in Campaign.query.filter_by(sponsor_id=current_user.id).all()]
    form.influencer_id.choices = [(user.id, user.username) for user in User.query.filter_by(role='influencer').all()]

    if form.validate_on_submit():
        ad_request.campaign_id = form.campaign_id.data
        ad_request.influencer_id = form.influencer_id.data
        ad_request.messages = form.messages.data
        ad_request.requirements = form.requirements.data
        ad_request.payment_amount = form.payment_amount.data
        ad_request.status = form.status.data
        db.session.commit()
        flash('Your ad request has been updated!', 'success')
        # return redirect(url_for('main.sponsor_dashboard'))
        return redirect(url_for('main.view_ad_requests'))
    elif request.method == 'GET':
        form.campaign_id.data = ad_request.campaign_id
        form.influencer_id.data = ad_request.influencer_id
        form.messages.data = ad_request.messages
        form.requirements.data = ad_request.requirements
        form.payment_amount.data = ad_request.payment_amount
        form.status.data = ad_request.status

    return render_template('create_ad_request.html', title='Update Ad Request', form=form, legend='Update Ad Request',form_action='main.update_ad_request', ad_request_id=ad_request_id)

@main.route("/sponsor/ad_request/<int:ad_request_id>/delete", methods=['POST'])
@login_required
@sponsor_required
def delete_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    db.session.delete(ad_request)
    db.session.commit()
    flash('Your ad request has been deleted!', 'success')
    return redirect(url_for('main.view_ad_requests'))

@main.route("/sponsor/ad_requests/search", methods=['GET', 'POST'])
@login_required
@sponsor_required
def search_ad_requests():
    search_form = SearchForm()
    ad_requests = []
    if search_form.validate_on_submit():
        search_query = search_form.search.data
        ad_requests = AdRequest.query.join(Campaign).filter(
            Campaign.sponsor_id == current_user.id,
            Campaign.name.ilike(f'%{search_query}%')
        ).all()
        flash(f'Search results for "{search_query}":', 'info')
    return render_template('search_ad_requests.html', ad_requests=ad_requests, search_form=search_form)

@main.route("/sponsor/ad_requests", methods=['GET'])
@login_required
@sponsor_required
def view_ad_requests():
    ad_requests = AdRequest.query.join(Campaign).filter(Campaign.sponsor_id == current_user.id).all()
    return render_template('view_ad_requests.html', ad_requests=ad_requests)

@main.route("/sponsor/ad_request/respond/<int:ad_request_id>", methods=['POST'])
@login_required
@sponsor_required
def respond_to_proposal(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    if ad_request.campaign.sponsor_id != current_user.id:
        flash('You do not have permission to respond to this proposal.', 'danger')
        return redirect(url_for('main.sponsor_dashboard'))
    
    action = request.form.get('action')
    if action == 'accept':
        ad_request.payment_amount = ad_request.proposed_amount
        ad_request.status = 'Approved'
        ad_request.negotiation_status = 'Closed'
        flash('The proposal has been accepted!', 'success')
    elif action == 'reject':
        ad_request.status = 'Rejected'
        ad_request.negotiation_status = 'Closed'
        flash('The proposal has been rejected.', 'danger')
    elif action == 'counter':
        counter_amount = request.form.get('counter_amount')
        ad_request.proposed_amount = float(counter_amount)
        ad_request.status = 'Negotiating'
        ad_request.negotiation_status = 'Open'
        flash('A counter proposal has been submitted!', 'info')
    
    db.session.commit()
    return redirect(url_for('main.sponsor_dashboard'))

#Influencer Dashboard

@main.route("/influencer/dashboard", methods=['GET', 'POST'])
@login_required
def influencer_dashboard():
    if current_user.role != 'influencer':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('main.home'))
    ad_requests = AdRequest.query.filter_by(influencer_id=current_user.id).all()
    profile = current_user.profile
    campaign_search_form = CampaignSearchForm()

    if campaign_search_form.validate_on_submit():
        search_query = campaign_search_form.search.data
        campaigns = Campaign.query.filter(
            Campaign.visibility == 'public',
            db.or_(
                Campaign.name.ilike(f'%{search_query}%'),
                Campaign.category.ilike(f'%{search_query}%'),
                Campaign.description.ilike(f'%{search_query}%')
            )
        ).all()
        flash(f'Search results for "{search_query}":', 'info')
        return render_template('search_campaigns.html', campaigns=campaigns, search_form=campaign_search_form)

    return render_template('influencer_dashboard.html', ad_requests=ad_requests, profile=profile, campaign_search_form=campaign_search_form)


@main.route("/influencer/profile", methods=['GET', 'POST'])
@login_required
@influencer_required
def influencer_profile():
    form = UpdateInfluencerProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        print(f"the profile :{current_user.profile}")
        if current_user.profile is None:
            profile = InfluencerProfile(
                user_id=current_user.id,
                name=form.name.data,
                category=form.category.data,
                niche=form.niche.data,
                reach=form.reach.data
            )
            db.session.add(profile)
        else:
            current_user.profile.name = form.name.data
            current_user.profile.category = form.category.data
            current_user.profile.niche = form.niche.data
            current_user.profile.reach = form.reach.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.influencer_dashboard'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        if current_user.profile:
            form.name.data = current_user.profile.name
            form.category.data = current_user.profile.category
            form.niche.data = current_user.profile.niche
            form.reach.data = current_user.profile.reach
    print(f"The current user : {current_user}")
    print(f"the user niche :{current_user.profile}")
    return render_template('influencer_profile.html', title='Update Profile', form=form, legend='Update Profile',profile=current_user.profile)


@main.route("/influencer/ad_request/<int:ad_request_id>/accept", methods=['POST'])
@login_required
@influencer_required
def accept_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    if ad_request.influencer_id != current_user.id:
        flash('You do not have permission to accept this ad request.', 'danger')
        return redirect(url_for('main.influencer_dashboard'))
    ad_request.status = 'Accepted'
    db.session.commit()
    flash('Ad request accepted.', 'success')
    return redirect(url_for('main.influencer_dashboard'))

@main.route("/influencer/ad_request/<int:ad_request_id>/reject", methods=['POST'])
@login_required
@influencer_required
def reject_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    if ad_request.influencer_id != current_user.id:
        flash('You do not have permission to reject this ad request.', 'danger')
        return redirect(url_for('main.influencer_dashboard'))
    ad_request.status = 'Rejected'
    db.session.commit()
    flash('Ad request rejected.', 'success')
    return redirect(url_for('main.influencer_dashboard'))

@main.route("/influencer/ad_request/<int:ad_request_id>/negotiate", methods=['POST'])
@login_required
@influencer_required
def negotiate_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    if ad_request.influencer_id != current_user.id:
        flash('You do not have permission to negotiate this ad request.', 'danger')
        return redirect(url_for('main.influencer_dashboard'))
    proposed_amount = request.form.get('proposed_amount')
    if proposed_amount:
        ad_request.proposed_amount = float(proposed_amount)
        db.session.add(proposed_amount)
        ad_request.status = "Negotiating"
        ad_request.negotiation_status = 'Open'
        
        db.session.commit()
        flash('Your proposed amount has been submitted!', 'success')
    
    return redirect(url_for('main.influencer_dashboard'))

@main.route("/influencer/profile/update", methods=['GET', 'POST'])
@login_required
@influencer_required
def update_influencer_profile():
    if current_user.role != 'influencer':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('main.home'))
    print(f"HERE HERE")
    form = UpdateInfluencerProfileForm()
    print(f"Request Method: {request.method}")
    print(f"Form Data: {form.data}")
    print(f"Form Errors: {form.errors}")
    if form.validate_on_submit():
        print(f"POST Request")
        print(f"Form Data: {form.data}")
        current_user.username = form.username.data
        current_user.email = form.email.data
        if current_user.profile is None:
            
            profile = InfluencerProfile(
                user_id=current_user.id,
                name=form.name.data,
                category=form.category.data,
                niche=form.niche.data,
                reach=form.reach.data
            )
            db.session.add(profile)
        else:
            print(f"The profile is {current_user.profile}")
            current_user.profile.name = form.name.data
            current_user.profile.category = form.category.data
            current_user.profile.niche = form.niche.data
            current_user.profile.reach = form.reach.data
            # db.session.add(profile)
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.influencer_dashboard'))
    elif request.method == 'GET':
        print(f"GET Request")
        if current_user.profile:
            print(f"The profile is {current_user.profile}")
            form.email.data = current_user.email
            form.username.data = current_user.username
            form.name.data = current_user.profile.name
            form.category.data = current_user.profile.category
            form.niche.data = current_user.profile.niche
            form.reach.data = current_user.profile.reach
    print(f"THERE THERE")
    return render_template('update_influencer_profile.html', title='Update Profile', form=form,profile=current_user.profile)

@main.route("/sponsor/influencers/search", methods=['GET', 'POST'])
@login_required
@sponsor_required
def search_influencers():
    search_form = InfluencerSearchForm()
    influencers = []
    if search_form.validate_on_submit():
        search_query = search_form.search.data
        influencers = User.query.join(InfluencerProfile).filter(
            User.role == 'influencer',
            db.or_(
                InfluencerProfile.name.ilike(f'%{search_query}%'),
                InfluencerProfile.category.ilike(f'%{search_query}%'),
                InfluencerProfile.niche.ilike(f'%{search_query}%')
            )
        ).all()
        flash(f'Search results for "{search_query}":', 'info')
    return render_template('search_influencers.html', influencers=influencers, search_form=search_form)

@main.route("/influencer/campaigns/search", methods=['GET', 'POST'])
@login_required
@influencer_required
def search_campaigns():
    if current_user.role != 'influencer':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('main.home'))
    search_form = CampaignSearchForm()
    campaigns = []
    if search_form.validate_on_submit():
        search_query = search_form.search.data
        campaigns = Campaign.query.filter(
            Campaign.visibility == 'public',
            db.or_(
                Campaign.name.ilike(f'%{search_query}%'),
                Campaign.category.ilike(f'%{search_query}%'),
                Campaign.description.ilike(f'%{search_query}%')
            )
        ).all()
        flash(f'Search results for "{search_query}":', 'info')
    return render_template('search_campaigns.html', campaigns=campaigns, search_form=search_form)

#Admin Dashboard

@main.route("/admin/dashboard")
@login_required
@admin_required
def admin_dashboard():
    users = User.query.all()
    campaigns = Campaign.query.all()
    ad_requests = AdRequest.query.all()

    # Statistics
    active_users_count = User.query.filter(User.role != 'admin').count()
    flagged_users_count = User.query.filter_by(is_flagged=True).count()
    active_campaigns_count = Campaign.query.count()
    active_ad_requests_count = AdRequest.query.count()
    flagged_campaigns_count = Campaign.query.filter_by(is_flagged=True).count()

    influencers_count = User.query.filter_by(role='influencer').count()
    sponsors_count = User.query.filter_by(role='sponsor').count()

    return render_template(
        'admin_dashboard.html',
        users=users,
        campaigns=campaigns,
        ad_requests=ad_requests,
        active_users_count=active_users_count,
        flagged_users_count=flagged_users_count,
        active_campaigns_count=active_campaigns_count,
        active_ad_requests_count=active_ad_requests_count,
        flagged_campaigns_count=flagged_campaigns_count,
        influencers_count=influencers_count,
        sponsors_count=sponsors_count
    )



@main.route("/admin/profile", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_profile():
    form = UpdateUserForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.admin_dashboard'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('admin_profile.html', title='Edit Profile', form=form, legend='Edit Profile')


@main.route("/admin/user/<int:user_id>/flag", methods=['POST'])
@login_required
@admin_required
def flag_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_flagged = True
    db.session.commit()
    flash(f'User {user.username} has been flagged.', 'success')
    return redirect(url_for('main.view_users'))

# Unflag a user
@main.route("/admin/user/<int:user_id>/unflag", methods=['POST'])
@login_required
@admin_required
def unflag_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_flagged = False
    db.session.commit()
    flash(f'User {user.username} has been unflagged.', 'success')
    return redirect(url_for('main.view_users'))

# Flag a campaign
@main.route("/admin/campaign/<int:campaign_id>/flag", methods=['POST'])
@login_required
@admin_required
def flag_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    campaign.is_flagged = True
    db.session.commit()
    flash(f'Campaign {campaign.name} has been flagged.', 'success')
    return redirect(url_for('main.admin_campaigns'))

# Unflag a campaign
@main.route("/admin/campaign/<int:campaign_id>/unflag", methods=['POST'])
@login_required
@admin_required
def unflag_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    campaign.is_flagged = False
    db.session.commit()
    flash(f'Campaign {campaign.name} has been unflagged.', 'success')
    return redirect(url_for('main.admin_campaigns'))

@main.route("/admin/users", methods=['GET'])
@login_required
@admin_required
def view_users():
    users = User.query.all()
    return render_template('view_users.html', users=users)

@main.route("/admin/user/new", methods=['GET', 'POST'])
@login_required
@admin_required
def new_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('New user has been created!', 'success')
        return redirect(url_for('main.view_users'))
    return render_template('create_user.html', title='Create User', form=form, legend='Create User')

@main.route("/admin/user/<int:user_id>/update", methods=['GET', 'POST'])
@login_required
@admin_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UpdateUserForm()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data
        db.session.commit()
        flash('User has been updated!', 'success')
        return redirect(url_for('main.view_users'))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.role.data = user.role
    return render_template('create_user.html', title='Update User', form=form, legend='Update User')

@main.route("/admin/user/<int:user_id>/delete", methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted!', 'success')
    return redirect(url_for('main.view_users'))

@main.route("/admin/campaigns")
@login_required
@admin_required
def admin_campaigns():
    campaigns = Campaign.query.all()
    return render_template('view_campaigns.html', campaigns=campaigns)


@main.route("/admin/campaign/new", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_new_campaign():
    form = CreateCampaignForm()
    form.sponsor_id.choices = [(sponsor.id, sponsor.username) for sponsor in User.query.filter_by(role='sponsor').all()]

    if form.validate_on_submit():
        campaign = Campaign(
            name=form.name.data,
            description=form.description.data,
            category=form.category.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            budget=form.budget.data,
            visibility=form.visibility.data,
            sponsor_id=form.sponsor_id.data,
            goals = form.goals.data
        )
        db.session.add(campaign)
        db.session.commit()
        flash('New campaign has been created!', 'success')
        return redirect(url_for('main.admin_dashboard'))
    return render_template('create_campaign.html', title='Create Campaign', form=form, legend='Create Campaign')


@main.route("/admin/campaign/<int:campaign_id>/update", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_update_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    form = CreateCampaignForm()
    form.sponsor_id.choices = [(user.id, user.username) for user in User.query.filter_by(role='sponsor').all()]

    if form.validate_on_submit():
        campaign.name = form.name.data
        campaign.description = form.description.data
        campaign.category = form.category.data
        campaign.start_date = form.start_date.data
        campaign.end_date = form.end_date.data
        campaign.budget = form.budget.data
        campaign.visibility = form.visibility.data
        campaign.sponsor_id = form.sponsor_id.data
        db.session.commit()
        flash('Campaign has been updated!', 'success')
        return redirect(url_for('main.admin_campaigns'))
    elif request.method == 'GET':
        form.name.data = campaign.name
        form.description.data = campaign.description
        form.category.data = campaign.category
        form.start_date.data = campaign.start_date
        form.end_date.data = campaign.end_date
        form.budget.data = campaign.budget
        form.visibility.data = campaign.visibility
        form.sponsor_id.data = campaign.sponsor_id
    return render_template('create_campaign.html', title='Update Campaign', form=form, legend='Update Campaign', form_action='main.admin_update_campaign', campaign_id=campaign.id)

@main.route("/admin/campaign/<int:campaign_id>/delete", methods=['POST'])
@login_required
@admin_required
def admin_delete_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    db.session.delete(campaign)
    db.session.commit()
    flash('Campaign has been deleted!', 'success')
    return redirect(url_for('main.admin_campaigns'))


@main.route("/admin/ad_requests", methods=['GET'])
@login_required
@admin_required
def admin_ad_requests():
    ad_requests = AdRequest.query.all()
    return render_template('admin_ad_requests.html', ad_requests=ad_requests)


@main.route("/admin/ad_request/new", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_new_ad_request():
    form = CreateAdRequestForm()
    form.campaign_id.choices = [(campaign.id, campaign.name) for campaign in Campaign.query.all()]
    form.influencer_id.choices = [(user.id, user.username) for user in User.query.filter_by(role='influencer').all()]

    if form.validate_on_submit():
        ad_request = AdRequest(
            campaign_id=form.campaign_id.data,
            influencer_id=form.influencer_id.data,
            messages=form.messages.data,
            requirements=form.requirements.data,
            payment_amount=form.payment_amount.data,
            status='Pending'
        )
        db.session.add(ad_request)
        db.session.commit()
        flash('New ad request has been created!', 'success')
        return redirect(url_for('main.admin_dashboard'))
    return render_template('create_ad_request.html', title='Create Ad Request', form=form, legend='Create Ad Request',form_action='main.admin_new_ad_request', ad_request_id=None)

@main.route("/admin/ad_request/<int:ad_request_id>/update", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_update_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    form = UpdateAdRequestForm()
    form.campaign_id.choices = [(campaign.id, campaign.name) for campaign in Campaign.query.all()]
    form.influencer_id.choices = [(user.id, user.username) for user in User.query.filter_by(role='influencer').all()]

    if form.validate_on_submit():
        ad_request.campaign_id = form.campaign_id.data
        ad_request.influencer_id = form.influencer_id.data
        ad_request.messages = form.messages.data
        ad_request.requirements = form.requirements.data
        ad_request.payment_amount = form.payment_amount.data
        ad_request.status = form.status.data
        db.session.commit()
        flash('Ad request has been updated!', 'success')
        return redirect(url_for('main.admin_ad_requests'))
    elif request.method == 'GET':
        form.campaign_id.data = ad_request.campaign_id
        form.influencer_id.data = ad_request.influencer_id
        form.messages.data = ad_request.messages
        form.requirements.data = ad_request.requirements
        form.payment_amount.data = ad_request.payment_amount
        form.status.data = ad_request.status
    return render_template('create_ad_request.html', title='Update Ad Request', form=form, legend='Update Ad Request', form_action='main.admin_update_ad_request', ad_request_id=ad_request.id)

@main.route("/admin/ad_request/<int:ad_request_id>/delete", methods=['POST'])
@login_required
@admin_required
def admin_delete_ad_request(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    db.session.delete(ad_request)
    db.session.commit()
    flash('Ad request has been deleted!', 'success')
    return redirect(url_for('main.admin_dashboard'))


@main.route("/admin/search", methods=['GET'])
@login_required
@admin_required
def admin_search():
    search_type = request.args.get('search_type')
    influencer_query = request.args.get('influencer')
    sponsor_query = request.args.get('sponsor')
    campaign_name_query = request.args.get('campaign_name')
    campaign_category_query = request.args.get('campaign_category')
    niche_query = request.args.get('niche')
    category_query = request.args.get('category')
    company_query = request.args.get('company')
    industry_query = request.args.get('industry')
    visibility_query = request.args.get('visibility')
    is_flagged = request.args.get('is_flagged')
    is_active = request.args.get('is_active')

    results = {
        'influencers': [],
        'sponsors': [],
        'campaigns': [],
    }

    if search_type == 'influencer':
        query = User.query.filter(User.role == 'influencer')
        if influencer_query:
            query = query.filter(User.username.contains(influencer_query))
        if niche_query:
            query = query.filter(User.niche.contains(niche_query))
        if category_query:
            query = query.filter(User.category.contains(category_query))
        if is_flagged:
            query = query.filter(User.is_flagged == True)
        results['influencers'] = query.all()

    elif search_type == 'sponsor':
        query = User.query.filter(User.role == 'sponsor')
        if sponsor_query:
            query = query.filter(User.username.contains(sponsor_query))
        if company_query:
            query = query.filter(User.company_name.contains(company_query))
        if industry_query:
            query = query.filter(User.industry.contains(industry_query))
        if is_flagged:
            query = query.filter(User.is_flagged == True)
        results['sponsors'] = query.all()

    elif search_type == 'campaign':
        query = Campaign.query
        if campaign_name_query:
            query = query.filter(Campaign.name.contains(campaign_name_query))
        if campaign_category_query:
            query = query.filter(Campaign.category.contains(campaign_category_query))
        if visibility_query:
            query = query.filter(Campaign.visibility.contains(visibility_query))
        if is_active:
            query = query.filter(Campaign.is_active == True)
        results['campaigns'] = query.all()

    return render_template('admin_search_results.html', results=results)

