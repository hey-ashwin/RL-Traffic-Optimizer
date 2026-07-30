from algorithms.sarsa_agent import SarsaAgent
from env.environment import TrafficEnv
import config
import numpy as np
import random

np.random.seed(42)
random.seed(42)

def run():
    env = TrafficEnv(config)
    agent = SarsaAgent(config)

    for episode in range(config.SARSA_EPISODES):
        state = env.reset()

        valid_actions = env.get_valid_actions()
        action = agent.choose_action(state, valid_actions)
        done = False
        total_reward = 0

        while not done:
            next_state, reward, done = env.step(action)
            total_reward += reward

            if done:
                next_action = None
            else:
                valid_actions = env.get_valid_actions()
                next_action = agent.choose_action(
                    next_state,
                    valid_actions
                )

            agent.learn(
                state,
                action,
                reward,
                next_state,
                next_action,
                done
            )

            state = next_state
            action = next_action

        agent.decay_epsilon()

        if (episode + 1) % 100 == 0:
            print(
                f"Episode {episode + 1}/{config.SARSA_EPISODES}"
                f" | Reward: {total_reward:.2f}"
                f" | Epsilon: {agent.epsilon:.2f}"
            )

    agent.save_q_table("q_tables/sarsa_q_table.pkl")

    print("\nTraining Complete!")
    print("Q-table saved.")

    print("Total Q-values:", agent.q_table.size)
    print("Non-zero Q-values:", np.count_nonzero(agent.q_table))

    return agent


if __name__ == "__main__":
    run()