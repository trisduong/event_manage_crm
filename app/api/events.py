from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.schemas.event import EventOut, EventCreate
from app.models.event import EventModel
from app.models.user import UserModel
from app.models.participation import ParticipationModel

router = APIRouter()


@router.post("/", response_model=EventOut)
def create_event(event: EventCreate):
    # Verify owner user exists if provided
    if event.owner:
        try:
            UserModel.get(event.owner)
        except UserModel.DoesNotExist:
            raise HTTPException(status_code=400, detail="Owner user not found")
    # Save the event
    event_item = EventModel(
        slug=event.slug,
        title=event.title,
        description=event.description or "",
        startAt=event.startAt,
        endAt=event.endAt,
        venue=event.venue or "",
        maxCapacity=event.maxCapacity,
        owner=event.owner or "",
        hosts=event.hosts or []
    )
    event_item.save()
    # Record owner and hosts as participants
    if event.owner:
        ParticipationModel(user_id=event.owner, event_id=event_item.id, role="host").save()
    for host_id in event.hosts or []:
        ParticipationModel(user_id=host_id, event_id=event_item.id, role="host").save()
    return event


@router.get("/", response_model=List[EventOut])
def list_events():
    events = []
    for e in EventModel.scan():
        events.append(EventOut(
            id=e.id,
            slug=e.slug,
            title=e.title,
            description=e.description,
            startAt=e.startAt,
            endAt=e.endAt,
            venue=e.venue,
            maxCapacity=e.maxCapacity,
            owner=e.owner,
            hosts=e.hosts
        ))
    return events


@router.post("/{event_id}/participate", response_model=dict)
def participate(event_id: str, user_id: str = Query(...)):
    # Add a user as an attendee to an event
    try:
        EventModel.get(event_id)
    except EventModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Event not found")
    try:
        UserModel.get(user_id)
    except UserModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    ParticipationModel(user_id=user_id, event_id=event_id, role="attendee").save()
    return {"message": "User added to event"}
