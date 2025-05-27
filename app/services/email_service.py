import uuid
from datetime import datetime
from app.models.outbox import EmailOutboxModel
from app.tasks.tasks import send_email_task


def queue_emails(user_ids, subject, body, utm_source=None, utm_medium=None, utm_campaign=None):
    """
    Create an outbox entry for each user and enqueue a Celery task to send the email.
    """
    for uid in user_ids:
        entry = EmailOutboxModel(
            id=str(uuid.uuid4()),
            created_at=datetime.utcnow(),
            recipient_id=uid,
            subject=subject,
            body=body,
            utm_source=utm_source,
            utm_medium=utm_medium,
            utm_campaign=utm_campaign,
            status="pending"
        )
        entry.save()
        # Enqueue Celery task for sending
        send_email_task.delay(entry.id)
