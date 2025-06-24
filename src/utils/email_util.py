import asyncio

from celery import Celery, shared_task
from celery.utils.log import get_task_logger
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

from src.configurations.settings import settings

logger = get_task_logger(__name__)

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
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="verify_user_template.html")


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_verification_email_task(self, to_email: str, data: dict):
    # to use this function, start celery using command: uv run celery -A src.utils.celery_worker.celery worker --loglevel=info
    try:
        asyncio.run(send_verification_url(to_email, data))
        logger.info(f"Verification email sent to {to_email}")
    except Exception as exc:
        logger.error(f"Failed to send verification email to {to_email}: {exc}")
        raise self.retry(exc=exc)
