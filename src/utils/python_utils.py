from datetime import datetime

# Uitlity function to make sure that datetimes are converted to iso so JSON works
def clean_datetimes(obj):
    if isinstance(obj, dict):
        return {k: clean_datetimes(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_datetimes(item) for item in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return obj
    