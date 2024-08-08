from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField,BooleanField,TextAreaField,DateField,FloatField,IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[ ('sponsor', 'Sponsor'), ('influencer', 'Influencer')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
    def validate_role(self, role):
        if role.data == 'admin':
            raise ValidationError('You cannot register as an admin.')
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class CampaignForm(FlaskForm):
    name = StringField('Campaign Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    budget = FloatField('Budget', validators=[DataRequired()])
    visibility = SelectField('Visibility', choices=[('public', 'Public'), ('private', 'Private')], validators=[DataRequired()])
    goals = TextAreaField('Goals', validators=[DataRequired()])
    submit = SubmitField('Create Campaign')

class SponsorProfileForm(FlaskForm):
    company_name = StringField('Company Name', validators=[Length(max=100)])
    industry = StringField('Industry', validators=[Length(max=100)])
    budget = FloatField('Budget')
    submit = SubmitField('Update Profile')
class SearchForm(FlaskForm):
    search = StringField('Search Campaigns', validators=[DataRequired()])
    submit = SubmitField('Search')

class CreateAdRequestForm(FlaskForm):
    campaign_id = SelectField('Campaign', coerce=int, validators=[DataRequired()])
    influencer_id = SelectField('Influencer', coerce=int, validators=[DataRequired()])
    messages = TextAreaField('Messages', validators=[DataRequired()])
    requirements = TextAreaField('Requirements', validators=[DataRequired()])
    payment_amount = FloatField('Payment Amount', validators=[DataRequired()])
    submit = SubmitField('Create Ad Request')

class UpdateAdRequestForm(FlaskForm):
    campaign_id = SelectField('Campaign', coerce=int, validators=[DataRequired()])
    influencer_id = SelectField('Influencer', coerce=int, validators=[DataRequired()])
    messages = TextAreaField('Messages', validators=[DataRequired()])
    requirements = TextAreaField('Requirements', validators=[DataRequired()])
    payment_amount = FloatField('Payment Amount', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Negotiating', 'Negotiating'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], validators=[DataRequired()])
    submit = SubmitField('Update Ad Request')
    negotiation_status = SelectField('Negotiation Status', choices=[('Open', 'Open'), ('Closed', 'Closed')], validators=[DataRequired()])
    
class UpdateInfluencerProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=60)])
    name = StringField('Name', validators=[DataRequired(), Length(min=6, max=60)])
    category = StringField('Category',)
    niche = StringField('Niche', )
    reach = IntegerField('Reach',)
    submit = SubmitField('Update Profile')

class InfluencerSearchForm(FlaskForm):
    search = StringField('Search Influencers', validators=[DataRequired()])
    submit = SubmitField('Search')

class CampaignSearchForm(FlaskForm):
    search = StringField('Search Campaigns', validators=[DataRequired()])
    submit = SubmitField('Search')


class CreateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=60)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[ ('sponsor', 'Sponsor'), ('influencer', 'Influencer')], validators=[DataRequired()])
    submit = SubmitField('Create User')

def validate_username( username):
    user = User.query.filter_by(username=username.data).first()
    if user:
        raise ValidationError('That username is taken. Please choose a different one.')

def validate_email( email):
    user = User.query.filter_by(email=email.data).first()
    if user:
        raise ValidationError('That email is taken. Please choose a different one.')

class UpdateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[ ('sponsor', 'Sponsor'), ('influencer', 'Influencer')], validators=[DataRequired()]) 
    submit = SubmitField('Update User')

class CreateCampaignForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    budget = FloatField('Budget', validators=[DataRequired()])
    visibility = SelectField('Visibility', choices=[('public', 'Public'), ('private', 'Private')], validators=[DataRequired()])
    sponsor_id = SelectField('Sponsor', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Create Campaign')
    goals = TextAreaField('Goals', validators=[DataRequired()])



