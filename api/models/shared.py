from datetime import datetime


def convert_date(date_string: str, time_string: str) -> datetime:
    """Converts a date and time strings to datetime object."""
    return datetime.strptime(date_string + "-" + time_string, '%Y-%m-%d-%H:%M')


def split_datetime(date: datetime) -> tuple[str, str]:
    """Splits the datetime to their equivalent date and time string."""
    return (
        None if date is None else date.strftime("%Y-%m-%d"),
        None if date is None else date.strftime("%H:%M")
    )


def validate(field, validator, exception, required=True):
    """Helper function for validating a given field."""
    if (required or field is not None) and not validator(field):
        raise exception


def notNone(value, default):
    """Returns the value if it is not None otherwise the default."""
    return value if value is not None else default
