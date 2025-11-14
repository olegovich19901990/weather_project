import random

def get_random_cnt(min_val = 1, max_val = 30):
    return random.randint(min_val, max_val)


def get_random_days(min_days = 1, max_days = 31):
    return random.randint(min_days, max_days)

def get_random_month(min_month = 1, max_month = 12):
    return random.randint(min_month, max_month)