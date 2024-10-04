from datetime import datetime


def convert_to_datetime(date_string: str) -> datetime:
    return datetime.strptime(date_string, "%Y-%m-%d")
