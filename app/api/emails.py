from fastapi import APIRouter, Query
from app.services.user_service import filter_users
from app.services.email_service import queue_emails
from app.schemas.email import EmailRequest

router = APIRouter()


@router.post("/send", response_model=dict)
def send_emails(
    email_req: EmailRequest,
    company: str | None = Query(None),
    jobTitle: str | None = Query(None),
    city: str | None = Query(None),
    state: str | None = Query(None),
    events_hosted_min: int | None = Query(None),
    events_hosted_max: int | None = Query(None),
    events_attended_min: int | None = Query(None),
    events_attended_max: int | None = Query(None),
    sort_by: str | None = Query(None),
    limit: int = Query(100, ge=1, le=1000)
):
    # Filter users by the given criteria
    users, _ = filter_users(
        company, jobTitle, city, state,
        events_hosted_min, events_hosted_max,
        events_attended_min, events_attended_max,
        sort_by, limit
    )
    user_ids = [u["id"] for u in users]
    # Queue emails (each user gets one email entry)
    queue_emails(
        user_ids,
        email_req.subject,
        email_req.body,
        email_req.utm_source,
        email_req.utm_medium,
        email_req.utm_campaign
    )
    return {"message": f"Queued email to {len(user_ids)} users"}
