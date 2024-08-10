from app import create_app

app,celery = create_app()
print(f"clerey : {celery}")
if __name__ == '__main__':
    app.run(debug=True)
