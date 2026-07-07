import env.reward_functions as rewards

# Simulation
LANE_LENGTH = 20
MAX_STEPS = 300
MIN_GREEN_TIME = 5

# Vehicle Generator Parameters
LAMBDA_N = 0.4
LAMBDA_S = 0.3
LAMBDA_E = 0.5
LAMBDA_W = 0.3



# Reward Functions
REWARD_FUNCTION = rewards.waiting_time_reward
 # or rewards.queue_length_reward
 # or rewards.composite_reward

"""
Note: REWARD_FUNCTION is a variable name, but that variable is not of type int or string...it is a function. 
IMP: it's NOT rewards.waiting_time_reward()
"""