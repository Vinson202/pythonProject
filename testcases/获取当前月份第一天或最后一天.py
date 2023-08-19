from datetime import datetime

import calendar

import time

# 获取当前月份的第一天
def first_day_of_month():

    # 获取当前日期和时间
    now = datetime.now()

    # 获取当前月份的第一天
    timestamp = datetime(now.year, now.month, 1)

    formatted_time = timestamp.strftime("%Y-%m-%d")
    # 打印结果
    # print("当前日期和时间：", now)
    # print("当前月份的第一天：", first_day_of_month)

    return formatted_time

print(first_day_of_month())

# 获取当前月份的最后一天
def last_day_of_month():
    # 获取当前日期和时间
    now = datetime.now()

    # 获取当前月份的最后一天
    last_day_of_month = calendar.monthrange(now.year, now.month)[1]

    # 构造最后一天的日期对象
    last_day = datetime(now.year, now.month, last_day_of_month)

    # 转化时间格式
    formatted_time = last_day.strftime("%Y-%m-%d")
    # 打印结果
    # print("当前日期和时间：", now)
    # print("当前月份的最后一天：", last_day)
    print("转化后的时间",formatted_time)

    return formatted_time

# print(last_day_of_month())



#转化时间格式
def current_time():

    #获取当前时间
    current_time = datetime.now()

    #将时间格式转化为年月日
    formatted_time = current_time.strftime("%Y-%m-%d")

    print("当前时间",current_time)
    print("转换后的时间",formatted_time)

# print(current_time())


