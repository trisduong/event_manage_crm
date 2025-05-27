import os
import uuid
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute, ListAttribute


class EventModel(Model):
    class Meta:
        table_name = "events"
        host = os.getenv("DYNAMODB_HOST", "http://localhost:4566")
        region = os.getenv("AWS_REGION", "us-east-1")

    id = UnicodeAttribute(hash_key=True, default=lambda: str(uuid.uuid4()))
    slug = UnicodeAttribute()
    title = UnicodeAttribute()
    description = UnicodeAttribute(null=True)
    startAt = UTCDateTimeAttribute()
    endAt = UTCDateTimeAttribute()
    venue = UnicodeAttribute(null=True)
    maxCapacity = NumberAttribute(default=0)
    owner = UnicodeAttribute(null=True)
    hosts = ListAttribute(of=UnicodeAttribute, null=True)
