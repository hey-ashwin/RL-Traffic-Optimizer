import config
from env.environment import TrafficEnv
from algorithms.fixed_time_agent import FixedTimeAgent


def run(time_period):

    env = TrafficEnv(config)
    agent = FixedTimeAgent(time_period)

    state = env.reset()
    done = False

    while not done:
        action = agent.choose_action(state)
        state, reward, done = env.step(action)

    remaining = sum(len(q) for q in env.queues.values())

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


