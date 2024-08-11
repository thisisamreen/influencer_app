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