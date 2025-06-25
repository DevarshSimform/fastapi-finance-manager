import asyncio

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

from src.configurations.settings import settings

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


def send_verification_email(to_email: str, data: dict):
    async def send():
        message = MessageSchema(
            subject="Verify yourself",
            recipients=[to_email],
            template_body=data,
            subtype="html",
        )
        fm = FastMail(conf)
        await fm.send_message(message, template_name="verify_user_template.html")

    asyncio.run(send())
