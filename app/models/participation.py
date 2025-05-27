import os
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute


class ParticipationModel(Model):
    class Meta:
        table_name = "participation"
        host = os.getenv("DYNAMODB_HOST", "http://localhost:4566")
        region = os.getenv("AWS_REGION", "us-east-1")

    user_id = UnicodeAttribute(hash_key=True)
    event_id = UnicodeAttribute(range_key=True)
    role = UnicodeAttribute(default="attendee")  # e.g. "attendee" or "host"
