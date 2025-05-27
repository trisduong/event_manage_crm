from typing import Optional
from app.models.user import UserModel
from app.models.event import EventModel
from app.models.participation import ParticipationModel


def filter_users(company: Optional[str] = None,
                 jobTitle: Optional[str] = None,
                 city: Optional[str] = None,
                 state: Optional[str] = None,
                 events_hosted_min: Optional[int] = None,
                 events_hosted_max: Optional[int] = None,
                 events_attended_min: Optional[int] = None,
                 events_attended_max: Optional[int] = None,
                 sort_by: Optional[str] = None,
                 limit: int = 10):
    """
    Scan UserModel with optional attribute filters, then apply hosted/attended range filters.
    Returns a list of user dicts (including events counts).
    """
    filter_cond = None
    if company:
        cond = (UserModel.company == company)
        filter_cond = cond if filter_cond is None else (filter_cond & cond)
    if jobTitle:
        cond = (UserModel.jobTitle == jobTitle)
        filter_cond = cond if filter_cond is None else (filter_cond & cond)
    if city:
        cond = (UserModel.city == city)
        filter_cond = cond if filter_cond is None else (filter_cond & cond)
    if state:
        cond = (UserModel.state == state)
        filter_cond = cond if filter_cond is None else (filter_cond & cond)

    users_iter = UserModel.scan(filter_condition=filter_cond) if filter_cond else UserModel.scan()
    result_list = []

    for user in users_iter:
        hosted_count = len(list(EventModel.scan(filter_condition=(EventModel.owner == user.id))))
        attended_count = len(list(ParticipationModel.query(hash_key=user.id)))
        # Apply hosted count filter
        if events_hosted_min is not None and hosted_count < events_hosted_min:
            continue
        if events_hosted_max is not None and hosted_count > events_hosted_max:
            continue
        # Apply attended count filter
        if events_attended_min is not None and attended_count < events_attended_min:
            continue
        if events_attended_max is not None and attended_count > events_attended_max:
            continue
        user_data = user.attribute_values
        user_data['events_hosted'] = hosted_count
        user_data['events_attended'] = attended_count
        result_list.append(user_data)

    # Sorting
    if sort_by:
        reverse = False
        if sort_by.startswith('-'):
            sort_by = sort_by[1:]
            reverse = True
        result_list.sort(key=lambda x: x.get(sort_by, ""), reverse=reverse)

    # Pagination (simple slicing)
    return result_list[:limit], None
