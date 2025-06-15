from datetime import datetime

def unix_time_to_date(unix_time: int) -> str:
    """Convert a Unix timestamp to a date string"""
    return datetime.fromtimestamp(unix_time).strftime("%Y-%m-%d %H:%M:%S")
