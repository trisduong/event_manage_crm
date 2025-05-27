import os
import uuid
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute


class UserModel(Model):
    class Meta:
        table_name = "users"
        host = os.getenv("DYNAMODB_HOST", "http://localhost:4566")
        region = os.getenv("AWS_REGION", "us-east-1")

    id = UnicodeAttribute(hash_key=True, default=lambda: str(uuid.uuid4()))
    firstName = UnicodeAttribute()
    lastName = UnicodeAttribute()
    phoneNumber = UnicodeAttribute(null=True)
    email = UnicodeAttribute()
    avatar = UnicodeAttribute(null=True)
    gender = UnicodeAttribute(null=True)
    jobTitle = UnicodeAttribute(null=True)
    company = UnicodeAttribute(null=True)
    city = UnicodeAttribute(null=True)
    state = UnicodeAttribute(null=True)


    # add global secondary index with email#gender#jobTitle#company#city#state as the key to support filter
