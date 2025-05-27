from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.schemas.user import UserOut, UserCreate
from app.models.user import UserModel
from app.services.user_service import filter_users

router = APIRouter()


@router.post("", response_model=UserOut)
def create_user(user: UserCreate):
    user_item = UserModel(
        firstName=user.firstName,
        lastName=user.lastName,
        email=user.email,
        phoneNumber=user.phoneNumber or "",
        avatar=user.avatar or "",
        gender=user.gender or "",
        jobTitle=user.jobTitle or "",
        company=user.company or "",
        city=user.city or "",
        state=user.state or ""
    )
    user_item.save()
    return user


@router.get("", response_model=List[UserOut])
def list_users(
    company: Optional[str] = Query(None),
    jobTitle: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    events_hosted_min: Optional[int] = Query(None),
    events_hosted_max: Optional[int] = Query(None),
    events_attended_min: Optional[int] = Query(None),
    events_attended_max: Optional[int] = Query(None),
    sort_by: Optional[str] = Query(None, description="Field name to sort by, prefix with '-' for descending"),
    limit: int = Query(10, ge=1, le=100)
):
    users, _ = filter_users(
        company, jobTitle, city, state,
        events_hosted_min, events_hosted_max,
        events_attended_min, events_attended_max,
        sort_by, limit
    )
    return [UserOut(**u) for u in users]
