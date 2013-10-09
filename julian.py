

def jtime(timenow=True, datetime_inst=False):
    import datetime
    if timenow:
            dt = datetime.datetime.utcnow() - datetime.datetime(2000, 1, 1, 12, 0)
    else:
        dt=datetime_inst - datetime.datetime(2000, 1, 1, 12, 0)
    return (dt.days + (dt.seconds + dt.microseconds / (1000000.0)) / (24 * 3600.0) + 2451545)
