from datetime import datetime, timedelta, timezone


def get_timezone_now():
    return datetime.now(timezone.utc)
