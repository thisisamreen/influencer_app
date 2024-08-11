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
        send_reminder_email(influencer) 
    print(f"All Reminders sent")


@celery.task(name="app.send_monthly_report")
def send_monthly_report():
    sponsors = User.query.filter_by(role='sponsor').all()
    for sponsor in sponsors:
        html_report = generate_monthly_report(sponsor)
        msg = Message(
            subject=f"Monthly Activity Report - {datetime.utcnow().strftime('%B %Y')}",
            recipients=[sponsor.email],
            html=html_report
        )
        mail.send(msg)
        print(f"Report sent to {sponsor.email}")
        print(f"Report: \n{msg}")
    # sponsor = User.query.get(sponsor_id)
    # if sponsor:
    #     html_report = generate_monthly_report(sponsor)
    #     msg = Message(
    #         subject=f"Monthly Activity Report - {datetime.utcnow().strftime('%B %Y')}",
    #         recipients=[sponsor.email],
    #         html=html_report
    #     )
    #     mail.send(msg)
    #     print(f"Report sent to {sponsor.email}")
    #     print(f"Report: \n{msg}")

@app.route('/daily-reminder-task')
def daily_reminder_task():
    send_daily_reminder()
    return jsonify({"status": "Task completed"})

@app.route('/monthly-report-task')
def monthly_report_task():
    send_monthly_report()
    return jsonify({"status": "Task completed"})




if __name__ == '__main__':
    app.run(debug=True)
    # celery.run()
