from src.utils.email_util import celery

celery.autodiscover_tasks(["src.utils.email_util"])
