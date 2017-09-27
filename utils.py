from datetime import datetime
from isolation.isolation import TIME_LIMIT_MILLIS

start_time = None
def time_left(stop=False):
    global start_time
    if stop:
        start_time = None
        return

    if start_time is None:
        start_time = datetime.now().microsecond/1000 +  1000*datetime.now().second
    current_time = datetime.now().microsecond/1000 +  1000*datetime.now().second
    return TIME_LIMIT_MILLIS - (current_time - start_time)

# time_left = lambda : time_limit - (time_millis() - move_start)