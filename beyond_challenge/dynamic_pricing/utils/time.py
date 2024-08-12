from datetime import datetime
from datetime import timedelta


def seconds_until_end_of_today():
    time_delta = (
        datetime.combine(
            datetime.now().date() + timedelta(days=1),
            datetime.strptime("0000", "%H%M").time(),
        )
        - datetime.now()
    )
    return time_delta.seconds
