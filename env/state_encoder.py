from enum import Enum

"""
Converts raw lane queues into density buckets to avoid state-space explosion in tabular RL methods.
"""

class Bucket(Enum):
    EMPTY = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4

def get_bucket(count):
    if count == 0:
        return Bucket.EMPTY
    elif count <= 3:
        return Bucket.LOW
    elif count <= 7:
        return Bucket.MEDIUM
    elif count <= 12:
        return Bucket.HIGH
    else:
        return Bucket.VERY_HIGH


def encode_state(queues):
    """
    queues: {"N": [...], "S": [...], "E": [...], "W": [...]}
    returns: {"N": "Bucket.EMPTY", "S": "Bucket.VERY_HIGH", "E": "Bucket.HIGH", "W": "Bucket.LOW"}
    """
    return {lane: get_bucket(len(cars)) for lane, cars in queues.items()}