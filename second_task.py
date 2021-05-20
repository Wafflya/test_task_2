from datetime import datetime

import pymongo
import random
import time
from pymongo import MongoClient

# Инициализация БД
client = MongoClient()
db = client.get_database('mongo')
accruals = db.accrual
payments = db.payment

# Генерация набора данных (делал для тестов)
"""
def str_time_prop(start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%m/%d/%Y %I:%M %p', prop)



n = random.randint(50, 100)
for i in range(n):
    r_d = random_date('1/1/2005 1:30 PM', '1/1/2020 4:50 AM', random.random())
    a = datetime.strptime(r_d, '%m/%d/%Y %I:%M %p')
    r_m = random.randint(1, 12)
    ac = {
        "date": a,
        "month": r_m
    }
    acc_id = accruals.insert_one(ac).inserted_id

n = random.randint(50, 100)
for i in range(n):
    r_d = random_date('1/1/2005 1:30 PM', '1/1/2020 4:50 AM', random.random())
    a = datetime.strptime(r_d, '%m/%d/%Y %I:%M %p')
    r_m = random.randint(1, 12)
    pay = {
        "date": a,
        "month": r_m
    }
    pay_id = payments.insert_one(pay).inserted_id
"""

used_pays = {}
unused_pays = set()
# Основной алгоритм. За О(n*logm) справляется
for pay in payments.find().sort("date"):
    f = True
    debt_def = 0
    for debt in accruals.find({'date': {'$lte': pay['date']}, '_id': {'$nin': list(used_pays.values())}}).sort("date",
                                                                                                               pymongo.DESCENDING):
        if debt['month'] == pay['month']:
            used_pays[pay['_id']] = debt['_id']
            f = False
            break
        debt_def = debt['_id']

    if not f:
        continue
    elif debt_def == 0:
        unused_pays.add(pay['_id'])
    else:
        used_pays[pay['_id']] = debt_def

# Инициализируем результирующие таблички
result_table = db.result
unused_payment = db.unused_payment

# И записываем в них список неиспользованных платежей
for i in unused_pays:
    item = payments.find_one({'_id': i})
    unused_payment_id = unused_payment.insert_one(item).inserted_id


# А также таблицу соответствий!
for key in used_pays:
    p = payments.find_one({'_id': key})
    ac = accruals.find_one({'_id': used_pays[key]})
    result_item = {
        'payment': p,
        'accrual': ac
    }
    result_id = result_table.insert_one(result_item).inserted_id
