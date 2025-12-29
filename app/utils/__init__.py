from datetime import datetime, time, timezone
from typing import Optional

def normalize_date_range(
    date_from: Optional[datetime],
    date_to: Optional[datetime],
    time_from: Optional[time] = None,
    time_to: Optional[time] = None
):
    start = None
    end = None

    if date_from:
        start = datetime.combine(
            date_from,
            time_from or time.min,
            tzinfo=timezone.utc
        )

    if date_to:
        end = datetime.combine(
            date_to,
            time_to or time.max,
            tzinfo=timezone.utc
        )

    return start, end
