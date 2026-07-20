from datetime import datetime

from database.models import Subscription

price_list = {
    "time": {
        1: 99,
        3: 279,
        6: 549
    }, 
    "device": {
        1: 39,
        3: 79,
        6: 149
    }
}

def calculate_buy(time: int, devices: int):
    return price_list["time"][time] + price_list["device"][time] * (devices - 1)

def calculate_add_device(sub: Subscription):
    remaining = (sub.expire_at - datetime.now()).days

    price = int(39 * (remaining / 30))

    if price <= 39:
        return 39
    
    if price >= 149:
        return 149
    
    return price

def calculate_renew(sub: Subscription, time: int, devices: int):
    if sub.hwid_device_limit >= devices:
        return calculate_buy(time, devices)
    
    return calculate_buy(time, devices) + \
        calculate_add_device(sub) * (devices - sub.hwid_device_limit)