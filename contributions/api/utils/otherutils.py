from datetime import datetime

"""
Get current time in UTC format.
"""
def get_current_time_utc():
    currenttime = datetime.utcnow()
    formattedtime, micro = currenttime.strftime('%Y-%m-%dT%H:%M:%S.%f').split('.')
    formattedtime = "%s.%03dZ" % (formattedtime, int(micro) / 1000)

    return formattedtime

