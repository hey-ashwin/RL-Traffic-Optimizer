from algorithms.sarsa_agent import SarsaAgent, _get_indices
from env import state_encoder
from env.environment import TrafficEnv
import config
import numpy as np
import random
from env.environment import Action

np.random.seed(42)
random.seed(42)

def run():
    env = TrafficEnv(config)
    agent = SarsaAgent(config)

    agent.load_q_table("q_tables/sarsa_q_table.pkl")

    state = env.reset()
    done = False
    total_reward = 0

    while not done:
        valid_actions = env.get_valid_actions()
        action = agent.choose_best_action(
            state,
            valid_actions
        )

        if action == Action.SWITCH:
            print(
                f"Step {env.current_step:3} | "
                f"N={len(env.queues['N']):2}, "
                f"S={len(env.queues['S']):2}, "
                f"E={len(env.queues['E']):2}, "
                f"W={len(env.queues['W']):2} | "
                f"Light={env.light_state.name} | "
                f"Phase={env.current_phase_duration}"
            )

        state, reward, done = env.step(action)

        total_reward += reward

    remaining = sum(
        len(queue)
        for queue in env.queues.values()
    )

    avg_wait = (
        env.total_waiting_time /
        max(env.total_cars_departed, 1)
    )

    throughput = (
        env.total_cars_departed /
        config.MAX_STEPS
    )


    remaining_wait = 0
    for direction in env.queues:
        for car in env.queues[direction]:
            remaining_wait += env.current_step - car.entry_time



    print("\nSARSA Evaluation")
    print("--------------------------")
    print("Reward        :", total_reward)
    print("Reward Function:", config.REWARD_FUNCTION.__name__)
    print("Cars Spawned  :", env.total_cars_spawned)
    print("Cars Departed :", env.total_cars_departed)
    print("Cars Remaining:", remaining)
    print("Average Wait  :", avg_wait)
    print("Throughput    :", throughput)
    print("Switches      :", env.total_switches)
    print("Remaining wait:", remaining_wait)


if __name__ == "__main__":
    run()