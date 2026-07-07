"""
Collection of reward functions for the traffic environment.

Each reward function accepts the current TrafficEnv object and
returns a single scalar reward.
"""


def waiting_time_reward(env):
    # Minimizes total vehicle waiting time
    waiting = 0

    for direction in env.queues:
        for car in env.queues[direction]:
            waiting += env.current_step - car.entry_time

    return -waiting


def queue_length_reward(env):
    # Minimizes queue lengths

    total_queue_length = 0

    for queue in env.queues.values():
        total_queue_length += len(queue)

    return -total_queue_length


def composite_reward(env):
    """
    Combines multiple traffic objectives.

    Reward =
        + throughput
        - queue length
        - waiting time

    The weights can be tuned experimentally.
    """

    waiting = 0

    for direction in env.queues:
        for car in env.queues[direction]:
            waiting += env.current_step - car.entry_time


    total_queue_length = 0

    for queue in env.queues.values():
        total_queue_length += len(queue)

    return (
        2 * env.cars_departed_last_step
        - 1 * total_queue_length
        - 0.2 * waiting
    )