# influencer_app
- Activate a virtual environment and install the requirements:

` pip install -r requirements.txt`

- To start the application, 
`cd influencer_app`
`python init_db.py` #to initialise the database
`python run.py`

- Run the application on http://127.0.0.1:5000

- Start the celery beat:
    `celery -A run.celery worker --loglevel=info`
    `celery -A run.celery beat --loglevel=info`

- MailHog: 
    - Local SMTP Server to test the mail service. It can catch all outgoing emails and allows to view them in a web interface without sending them to real email addresses.
    - Install "mailhog"
    - Run command in terminal:
        `mailhog`
    - Set the mail server to point to MailHog in config.py
        `MAIL_SERVER = 'localhost'
        MAIL_PORT = 1025
        MAIL_USE_TLS = False
        MAIL_USERNAME = None
        MAIL_PASSWORD = None`
    - View the captured emails by navigating to http://localhost:8025 in your web browser.