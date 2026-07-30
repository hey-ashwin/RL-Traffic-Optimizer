from env.environment import Action

class FixedTimeAgent:
    def __init__(self, time_period = 30):
        self.time_period = time_period

    def choose_action(self, state):         # this state is from get_raw_state in environment.py
        if state["phase_duration"] >= self.time_period:
            return Action.SWITCH

        return Action.KEEP