import numpy as np
from env.car import Car
from env.vehicle_generator import VehicleGenerator
from enum import Enum

class Action(Enum):
    KEEP = 0
    SWITCH = 1

class Light(Enum):
    NS = 0
    EW = 1

class TrafficEnv:
    def __init__(self, config):

        # Save Configuration
        self.config = config

        # Vehicle Generator
        self.generator = VehicleGenerator(config.LAMBDA_N, config.LAMBDA_S, config.LAMBDA_E, config.LAMBDA_W)
        # max_spawn_per_step argument currently not passed

        # Start the first episode
        self.reset()


    # FOR DEBUGGING ###############################################
    def print_state(self):
        print(f"Step: {self.current_step}")
        print(f"Light: {self.light_state.name}")
        print(f"Phase Duration: {self.current_phase_duration}")

        print(f"N: {self.queues['N']}")
        print(f"S: {self.queues['S']}")
        print(f"E: {self.queues['E']}")
        print(f"W: {self.queues['W']}")
    # #############################################################

    def get_raw_state(self):
        newQueues = {}
        for direction in self.queues:
            newQueues[direction] = self.queues[direction].copy()      # we're using a copy coz we don't want visualizer or smth to accidentally
                                                                                # erase the original env queues
        return {
            "queues": newQueues,
            "light": self.light_state,
            "phase_duration": self.current_phase_duration,
            "current_step": self.current_step
        }

    def reset(self):
        """
        NOTE: THE FOLLOWING LINES ARE UNDERLINED SHOWING A WEAK WARNING BECAUSE THESE ARE NOT DEFINED IN __init__
        BUT IT'S NOT A PROBLEM HERE BECAUSE EVERY CALL TO __init__ IS GUARANTEED TO CALL self.reset WHICH WILL INITIALIZE THESE
        """

        # Simulation State
        self.queues = {             # NOTE THIS QUEUE WILL HOLD OBJECTS OF CAR CLASS, NOT INTEGER COUNTS
            "N": [],
            "S": [],
            "E": [],
            "W": []
        }
        self.light_state = Light.NS         # this can be one of the 2 enums...showing which road is green
        self.current_phase_duration = 0
        self.current_step = 0

        # Statistics
        self.cars_departed_last_step = 0
        self.total_cars_departed = 0
        self.total_cars_spawned = 0
        self.total_switches = 0
        self.cumulative_reward = 0
        self.total_waiting_time = 0
        self.max_queue_length_reached = 0       # not using this currently

        return self.get_raw_state()

    def step(self, action):
        self._apply_action(action)
        self._move_vehicles()
        self._spawn_new_vehicles()
        reward = self._compute_reward()

        self.current_step += 1
        self.current_phase_duration += 1

        # Check if episode finished
        done = self.current_step >= self.config.MAX_STEPS

        return self.get_raw_state(), reward, done


    # the following function names start with _ bcoz they are internal functions & need to be called from outside
    
    # Apply Action             
    def _apply_action(self, action):
        if action == Action.SWITCH and self.current_phase_duration >= self.config.MIN_GREEN_TIME:
            if self.light_state == Light.NS:
                self.light_state = Light.EW
            else:
                self.light_state = Light.NS

            self.current_phase_duration = 0
            self.total_switches += 1

    # Move Vehicles
    def _move_vehicles(self):
        self.cars_departed_last_step = 0

        if self.light_state == Light.NS:
            if self.queues["N"]:
                car = self.queues["N"].pop(0)
                wait = self.current_step - car.entry_time
                self.total_cars_departed += 1
                self.cars_departed_last_step += 1
                self.total_waiting_time += wait

            if self.queues["S"]:
                car = self.queues["S"].pop(0)
                wait = self.current_step - car.entry_time
                self.total_cars_departed += 1
                self.cars_departed_last_step += 1
                self.total_waiting_time += wait

        else:
            if self.queues["E"]:
                car = self.queues["E"].pop(0)
                wait = self.current_step - car.entry_time
                self.total_cars_departed += 1
                self.cars_departed_last_step += 1
                self.total_waiting_time += wait

            if self.queues["W"]:
                car = self.queues["W"].pop(0)
                wait = self.current_step - car.entry_time
                self.total_cars_departed += 1
                self.cars_departed_last_step += 1
                self.total_waiting_time += wait

    # Spawn New Vehicles
    def _spawn_new_vehicles(self):
        newCars = self.generator.generate()

        for direction in self.queues:
            for _ in range(newCars[direction]):
                if len(self.queues[direction]) < self.config.LANE_LENGTH:
                    self.queues[direction].append(Car(self.current_step))
                    self.total_cars_spawned += 1

    # Compute Reward
    def _compute_reward(self):
        return self.config.REWARD_FUNCTION(self)

    # Prevents rapid switching
    def get_valid_actions(self):
        if self.current_phase_duration < self.config.MIN_GREEN_TIME:
            return [Action.KEEP]

        return [Action.KEEP, Action.SWITCH]