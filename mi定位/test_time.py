import time
import datetime
import random
def get_sleep_time(h):
    # 第二天日期
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    print(tomorrow)
    # 第二天7点时间戳
    tomorrow_run_time = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d'))) + (h*3600)
    print(tomorrow_run_time)
    # print(tomorrow_run_time)
    # 当前时间戳
    current_time = int(time.time())
    # print(current_time)
    return tomorrow_run_time - current_time
# t = get_sleep_time(7)
# print(t)

# step = random.randint(11000,14000)  # 随机8000-10000步数
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))