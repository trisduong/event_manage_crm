from fastapi import FastAPI
from app.api import users, events, emails
from app.models.user import UserModel
from app.models.event import EventModel
from app.models.participation import ParticipationModel
from app.models.outbox import EmailOutboxModel

app = FastAPI(title="Event Management Platform")

@app.on_event("startup")
def create_tables():
    # Create DynamoDB tables if they do not exist (using LocalStack)
    if not UserModel.exists():
        UserModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    if not EventModel.exists():
        EventModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    if not ParticipationModel.exists():
        ParticipationModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    if not EmailOutboxModel.exists():
        EmailOutboxModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(events.router, prefix="/events", tags=["events"])
app.include_router(emails.router, prefix="/emails", tags=["emails"])
