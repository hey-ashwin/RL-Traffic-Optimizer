import config
from env.environment import TrafficEnv, Action
from env.car import Car

# env = TrafficEnv(config)
#
# print("Initial State")
# env.print_state()
#
# env.reset()
#
# env.step(Action.SWITCH)
#
# env.print_state()
#
# for i in range (10):
#     env.step(Action.KEEP)
#     env.print_state()
#


env = TrafficEnv(config)

env.queues["N"] = [Car(0), Car(4)]
env.queues["S"] = []
env.queues["E"] = [Car(8)]
env.queues["W"] = []

env.current_step = 10

print(env._compute_reward())