import config
from env.environment import TrafficEnv
from algorithms.fixed_time_agent import FixedTimeAgent
import numpy as np
import random

np.random.seed(42)
random.seed(42)

def run(time_period=10):

    env = TrafficEnv(config)
    agent = FixedTimeAgent(time_period)

    state = env.reset()
    done = False
    total_reward = 0

    while not done:
        action = agent.choose_action(state)
        state, reward, done = env.step(action)
        total_reward += reward

    remaining = sum(len(q) for q in env.queues.values())

    avg_wait = (env.total_waiting_time/max(env.total_cars_departed, 1))

    throughput = (env.total_cars_departed/config.MAX_STEPS)

    remaining_wait = 0
    for direction in env.queues:
        for car in env.queues[direction]:
            remaining_wait += env.current_step - car.entry_time



    print("\nFixed-Time Evaluation")
    print("--------------------------")
    print("Time Period    :", time_period)
    print("Reward Function:", config.REWARD_FUNCTION.__name__)
    print("Reward         :", total_reward)
    print("Cars Spawned   :", env.total_cars_spawned)
    print("Cars Departed  :", env.total_cars_departed)
    print("Cars Remaining :", remaining)
    print("Average Wait   :", avg_wait)
    print("Throughput     :", throughput)
    print("Switches       :", env.total_switches)
    print("Remaining wait:", remaining_wait)

    return {
        "time_period": time_period,
        "spawned": env.total_cars_spawned,
        "departed": env.total_cars_departed,
        "remaining": remaining,
        "avg_wait": env.total_waiting_time / max(env.total_cars_departed, 1),
        "throughput": env.total_cars_departed / config.MAX_STEPS,
        "avg_arrivals_per_step": env.total_cars_spawned / config.MAX_STEPS,
        "switches": env.total_switches
    }

if __name__ == "__main__":
    run()

