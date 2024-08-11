# from app import celery, create_app

# app = create_app()
# celery = celery

# if __name__ == '__main__':
#     celery.start()
from run import app,celery

if __name__ == '__main__':
    celery.start()