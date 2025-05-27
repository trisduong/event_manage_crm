import os
import uuid
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute


class EmailOutboxModel(Model):
    class Meta:
        table_name = "email_outbox"
        host = os.getenv("DYNAMODB_HOST", "http://localhost:4566")
        region = os.getenv("AWS_REGION", "us-east-1")

    id = UnicodeAttribute(hash_key=True, default=lambda: str(uuid.uuid4()))
    created_at = UTCDateTimeAttribute()
    recipient_id = UnicodeAttribute()
    subject = UnicodeAttribute()
    body = UnicodeAttribute()
    utm_source = UnicodeAttribute(null=True)
    utm_medium = UnicodeAttribute(null=True)
    utm_campaign = UnicodeAttribute(null=True)
    status = UnicodeAttribute(default="pending")  # pending, sent, or failed
