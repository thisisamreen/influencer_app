Influencer Engagement and Sponsorship Coordination Platform
## Overview
This is an Influencer Engagement and Sponsorship Coordination Platform that allows sponsors to manage campaigns and ad requests, influencers to respond to ad requests, and an admin to manage users and view reports. The platform uses Flask as the web framework, Celery for asynchronous task management, Redis as a message broker, and MailHog for testing email functionalities.

## Features
User Roles: Admin, Sponsor, Influencer
Campaign Management: Sponsors can create, update, and delete campaigns.
Ad Request Management: Sponsors can send ad requests to influencers.
Influencer Actions: Influencers can accept, reject, or negotiate ad requests.
Automated Tasks:
Daily reminders for influencers.
Monthly activity reports for sponsors.
CSV Export: Sponsors can export campaign details as a CSV file.
Email Notifications: Using MailHog for testing email functionalities.


## Prerequisites
Ensure you have the following installed:

Python 3.8+
Redis server
MailHog (for testing emails)
Celery


## Setting Up the Project
1. Clone the Repository:

```
git clone https://github.com/your-repository/influencer-platform.git
cd influencer-platform
```
2. Create and Activate a Virtual Environment:
```
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. Install Dependencies:
```
pip install -r requirements.txt

```
4. Environment Variables:
    - Create a .env file in the root directory with the following content:
```
EMAIL_USER=your-name
EMAIL_PASS=your-email-password
MAIL_DEFAULT_SENDER=your-email@examle.com
RECIPIENTS_EMAIL=example@examle.com
```

    - Adjust other configuration parameters as needed.

5. Initialize & Populate the Database:

```
python init_db.py

```

## Running the Application
**Option 1:** Using a Shell Script (Linux/MacOS) or Batch Script (Windows)
1. Run All Services:
- For Linux/MacOS:
    ```
    ./start_app.sh
    ```
- For Windows:
```
start_app.bat
```
**Option 2:** Running Services Manually
1. Start Redis Server:
```
redis-server
```
2. Start MailHog:
```
mailhog
```

    - MailHog Web Interface: http://localhost:8025
3. Start Celery Worker:
```
celery -A run.celery worker --loglevel=info
```
4. Start Celery Beat:
```
celery -A app.celery beat --loglevel=info
```
5. Run Flask Application:

```python run.py```

## Usage
- Access the Application:

- Visit http://localhost:5000 in your browser.
- Login as a Sponsor:
    Manage campaigns, view ad requests, and download CSV reports.
- Login as an Influencer:
    Respond to ad requests and view available campaigns.
- Admin Role:
    Manage users and view overall platform reports.


## Testing Email Functionality
- MailHog:
    All outgoing emails are captured by MailHog.
    View captured emails: http://localhost:8025.


1. Daily Reminders:
    Automatically sent to influencers who haven't visited or responded to ad requests.
2. Monthly Activity Reports:
    Automatically generated and sent to sponsors on the first day of each month.
3. CSV Export:
    Sponsors can download campaign details as a CSV file from their dashboard.





