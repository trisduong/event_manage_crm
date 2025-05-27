from app.tasks.celery_app import celery_app
from app.models.outbox import EmailOutboxModel
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from app.core.config import settings


@celery_app.task
def send_email_task(outbox_id: str):
    # Fetch the email outbox entry
    try:
        outbox = EmailOutboxModel.get(outbox_id)
    except EmailOutboxModel.DoesNotExist:
        return
    if outbox.status != "pending":
        return

    # Use AWS SES (LocalStack) to send the email
    ses = boto3.client(
        "ses",
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.aws_region,
        endpoint_url=settings.ses_host,
        config=Config(retries={"max_attempts": 3})
    )
    try:
        ses.send_email(
            Source="noreply@example.com",
            Destination={"ToAddresses": [outbox.recipient_id]},
            Message={
                "Subject": {"Data": outbox.subject},
                "Body": {"Text": {"Data": outbox.body}}
            }
        )
        outbox.status = "sent"
        outbox.save()
    except ClientError:
        outbox.status = "failed"
        outbox.save()
