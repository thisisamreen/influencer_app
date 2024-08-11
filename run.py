from flask import jsonify
from app import create_app,make_celery
from tasks import *
app = create_app()
celery = make_celery(app)

@celery.task(name="app.send_daily_reminder")
def send_daily_reminder():
    print(f"Task is running..")
    influencers_to_remind = get_influencers_with_pending_requests()

    for influencer in influencers_to_remind:
        send_reminder(influencer) 
    print(f"All Reminders sent")

@app.route('/start-task')
def start_task():
    # result = send_daily_reminder.apply_async()
    send_daily_reminder()
    return jsonify({"status": "Task completed"})
if __name__ == '__main__':
    app.run(debug=True)
    # celery.run()
