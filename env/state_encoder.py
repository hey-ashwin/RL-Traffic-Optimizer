"""
Converts raw lane queues into a compact state representation
using the total queues on the two roads.
"""

def encode_state(queues):
    """
    queues: {"N": [...], "S": [...], "E": [...], "W": [...]}

    returns:
    {
        "NS": 7,
        "EW": 12
    }
    """

    ns = len(queues["N"]) + len(queues["S"])
    ew = len(queues["E"]) + len(queues["W"])

    return {
        "NS": ns,
        "EW": ew
    }