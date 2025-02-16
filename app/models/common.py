from datetime import datetime

def get_datetime():
    """
    We specifically do NOT want to store timezone info
    in the datetime object since we don't need it.  Rather,
    we are treating datetime like a timestamp.
    """
    return datetime.now().replace(tzinfo=None)
