from datetime import datetime, time, timezone

def normalize_date_range(date_from, date_to):
    start = None
    end = None

    if date_from:
        start = datetime.combine(
            date_from, time.min, tzinfo=timezone.utc
        )

    if date_to:
        end = datetime.combine(
            date_to, time.max, tzinfo=timezone.utc
        )

    return start, end
