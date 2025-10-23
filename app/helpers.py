from datetime import datetime
import pytz

def get_current_time(tz_name: str):
    tz = pytz.timezone(tz_name)
    return datetime.now(tz)

def convert_timezone(dt, target_tz):
    tz = pytz.timezone(target_tz)
    return dt.astimezone(tz)
