import numpy as np
import random
import env.state_encoder as state_encoder
from config import MIN_GREEN_TIME
from env.environment import Action
import pickle

def _get_indices(state):
    raw_queues = state["queues"]
    encoded_queues = state_encoder.encode_state(raw_queues)
    ns = encoded_queues["NS"]
    ew = encoded_queues["EW"]

    ns = min(ns, 40)
    ew = min(ew, 40)

    current_light = state["light"].value

    can_switch = int(state["phase_duration"] >= MIN_GREEN_TIME)

    return ns, ew, current_light, can_switch

def _greedy_action(q_values, valid_actions):
    best_q = -float("inf")
    best_actions = []

    for action in valid_actions:
        q = q_values[action.value]
        if q > best_q:
            best_q = q
            best_actions = [action]
        elif q == best_q:
            best_actions.append(action)

    return random.choice(best_actions)


class SarsaAgent:
    def __init__(self, config):
        self.alpha = config.SARSA_ALPHA
        self.gamma = config.SARSA_GAMMA
        self.epsilon = config.SARSA_EPSILON_START
        self.epsilon_min = config.SARSA_EPSILON_MIN
        self.epsilon_decay = config.SARSA_EPSILON_DECAY
        self.q_table = np.zeros(shape= (41,41,2,2,2))   # first 2 dimensions for lane counts, 3rd for current light
                                                            # 4th for seeing if switching is allowed or not, 5th for action keep/switch


    def choose_action(self, state, valid_actions):     # chooses epsilon-greedy action
        ns, ew, current_light, can_switch = _get_indices(state)

        p = random.random()             # generates a random float in [0,1) -- NOTE THIS IS A HALF OPEN INTERVAL

        if p > self.epsilon:
            q_values = self.q_table[ns,ew,current_light,can_switch]
            action = _greedy_action(q_values, valid_actions)
        else:
            action = random.choice(valid_actions)

        return action


    def choose_best_action(self, state, valid_actions):        # returns the optimal action
        ns,ew,current_light,can_switch = _get_indices(state)

        q_values = self.q_table[ns, ew, current_light, can_switch]
        return _greedy_action(q_values, valid_actions)


    def learn(self, state, action, reward, next_state, next_action, done):
        ns, ew, light, can_switch = _get_indices(state)
        next_ns, next_ew, next_light, next_can_switch = _get_indices(next_state)

        current_q = self.q_table[ns, ew, light, can_switch, action.value]

        if done:
            target = reward
        else:
            next_q = self.q_table[next_ns, next_ew, next_light, next_can_switch, next_action.value]
            target = reward + self.gamma * next_q

        self.q_table[ns, ew, light, can_switch, action.value] += self.alpha * (target - current_q)

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon*self.epsilon_decay)

    def save_q_table(self, filepath):
        with open(filepath, "wb") as file:
            pickle.dump(self.q_table, file)

    def load_q_table(self, filepath):
        with open(filepath, "rb") as file:
            self.q_table = pickle.load(file)