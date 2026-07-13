"""
Converts raw lane queues into density buckets to avoid state-space explosion in tabular RL methods.
"""

def get_bucket(count):
    if count == 0:
        return "Empty"
    elif count <= 3:
        return "Low"
    elif count <= 7:
        return "Medium"
    elif count <= 12:
        return "High"
    else:
        return "Very High"


def encode_state(queues):
    """
    queues: {"N": [...], "S": [...], "E": [...], "W": [...]}
    returns: {"N": "Medium", "S": "Empty", "E": "High", "W": "Low"}
    """
    return {lane: get_bucket(len(cars)) for lane, cars in queues.items()}