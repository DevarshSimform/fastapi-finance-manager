import asyncio

from celery import Celery, shared_task
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

from src.configurations.settings import settings

celery = Celery("worker", broker=settings.REDIS_BROKER_URL)

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=settings.TEMPLATE_PATH,
)


# @celery.task
async def send_verification_url(to_email: str, data: dict):
    message = MessageSchema(
        subject="Verify yourself",
        recipients=[to_email],
        template_body=data,
        subtype="html",
        from_email=conf.MAIL_FROM,
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="verify_user_template.html")


@shared_task
def send_verification_email_task(to_email: str, data: dict):

    # to use this function, start celery using command: uv run celery -A src.utils.celery_worker.celery worker --concurrency=4 --loglevel=info
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:  # no loop in current thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.run_until_complete(send_verification_url(to_email, data))


# When need to specify queue name
# uv run celery -A src.utils.celery_worker.celery worker --concurrency=4 --loglevel=info
# send_verification_email_task.apply_async(args=[user_data.email, data], queue="email")
