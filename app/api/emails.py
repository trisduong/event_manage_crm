from fastapi import APIRouter, Query
from collections import Counter

from app.services.user_service import filter_users
from app.services.email_service import queue_emails
from app.models.outbox import EmailOutboxModel
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


@router.get("/analytics")
def email_status_analytics(
    utm_source: str | None = Query(None),
    utm_medium: str | None = Query(None),
    utm_campaign: str | None = Query(None),
):
    """
    Return count of emails grouped by status (sent, failed, pending),
    optionally filtered by UTM parameters.
    """
    status_counter = Counter()

    scan_filter = {}
    if utm_source:
        scan_filter["utm_source"] = utm_source
    if utm_medium:
        scan_filter["utm_medium"] = utm_medium
    if utm_campaign:
        scan_filter["utm_campaign"] = utm_campaign

    if scan_filter:
        emails = EmailOutboxModel.scan(filter_condition=(
            (EmailOutboxModel.utm_source == scan_filter.get("utm_source")) if "utm_source" in scan_filter else None
        ) & (
            (EmailOutboxModel.utm_medium == scan_filter.get("utm_medium")) if "utm_medium" in scan_filter else None
        ) & (
            (EmailOutboxModel.utm_campaign == scan_filter.get("utm_campaign")) if "utm_campaign" in scan_filter else None
        ))
    else:
        emails = EmailOutboxModel.scan()

    for email in emails:
        status_counter[email.status] += 1

    return {
        "summary": {
            "sent": status_counter.get("sent", 0),
            "failed": status_counter.get("failed", 0),
            "pending": status_counter.get("pending", 0),
        }
    }
