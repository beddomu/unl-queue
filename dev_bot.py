import datetime

import pytz

now = datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp(), pytz.timezone('Europe/London'))
if 0 <= now.weekday() <= 4:
    print("it's a weekday")
    if datetime.time(19) <= now.time() <= datetime.time(22):
        print("and it's in range")