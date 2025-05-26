import datetime

def validate_year(year):
    if not isinstance(year, int) or year < datetime.date.today().year or year > datetime.date.today().year + 2:
        raise ValueError("INVALID_YEAR")

def validate_month(month):
    if not isinstance(month, int) or not 1 <= month <= 12:
        raise ValueError("INVALID_MONTH")

def validate_day(day):
    if not isinstance(day, int) or not 1 <= day <= 31:
        raise ValueError("INVALID_DAY")

def validate_hour(hour):
    if not isinstance(hour, int) or not 0 <= hour <= 23:
        raise ValueError("INVALID_HOUR")

def validate_minute(minute):
    if not isinstance(minute, int) or not 0 <= minute <= 59:
        raise ValueError("INVALID_MINUTE")
