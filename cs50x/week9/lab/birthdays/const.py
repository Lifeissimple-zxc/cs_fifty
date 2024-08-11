ERROR_MESSAGES = {
    "NO_NAME": "Name was not provided, cannot add birthday data to the database :(",
    "INVALID_MONTH": "Month is incorrect. Needs to be between 1 and 12 (inclusive)",
    "INVALID_DAY": "Day is incorrect. Needs to be between 1 and 31 (inclusive)"
}

ALLOWED_DAYS = {
    1: list(range(1, 32)),
    2: list(range(1, 29)),
    3: list(range(1, 32)),
    4: list(range(1, 31)),
    5: list(range(1, 32)),
    6: list(range(1, 31)),
    7: list(range(1, 32)),
    8: list(range(1, 32)),
    9: list(range(1, 31)),
    10: list(range(1, 32)),
    11: list(range(1, 31)),
    12: list(range(1, 32))
}



