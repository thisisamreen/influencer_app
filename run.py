from flask import jsonify,url_for,request,redirect
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


@celery.task(name="app.export_campaigns_csv")
def export_campaigns_csv(sponsor_id):
    return export_campaigns(sponsor_id)

@app.route('/daily-reminder-task')
def daily_reminder_task():
    send_daily_reminder()
    return jsonify({"status": "Task completed"})

@app.route('/monthly-report-task')
def monthly_report_task():
    send_monthly_report()
    return jsonify({"status": "Task completed"})


# @app.route('/export-csv', methods=['POST'])
@app.route("/export-csv", methods=['POST'])
def export_csv():
    sponsor_id = request.form.get('sponsor_id')
    if not sponsor_id:
        return jsonify({"error": "Sponsor ID is required"}), 400

    result = export_campaigns_csv(sponsor_id)

    if result:
        return result
    else:
        return jsonify({"error": "Sponsor not found"}), 404
 
@app.route('/task-status/<task_id>')
def check_task_status(task_id):
    task = export_campaigns_csv.AsyncResult(task_id)
    status = task.status
    result = task.result if status == 'SUCCESS' else None

    return jsonify({"status": status, "result": result})


if __name__ == '__main__':
    app.run(debug=True)
    # celery.run()
