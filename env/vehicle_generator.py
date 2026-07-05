import numpy as np

"""
set lambdas to something small like 0.3 to avoid large instant queue buildup
for rush hour maybe increase lamba on some specific lanes. we can also do like if currTime < 300 then higher lambda
"""

class VehicleGenerator:
    def __init__(self, lambda_n, lambda_s, lambda_e, lambda_w, max_spawn_per_step=2):
        self.lambdas = {
            "N": lambda_n,
            "S": lambda_s,
            "E": lambda_e,
            "W": lambda_w
        }
        self.max_spawn_per_step = max_spawn_per_step

    def generate(self):
        """
        Samples from a Poisson distribution for each direction
        and clips the results to ensure realistic spawning.

        Simulation timestep = 1 second.
        Arrivals follow a Poisson process with mean λ per second.
        To avoid unrealistic bursts caused by the long tail of the
        Poisson distribution, arrivals are capped at max_spawn_per_step.
        """

        spawns = {}
        for direction, lam in self.lambdas.items():
            # Sample from Poisson distribution
            raw_spawn = np.random.poisson(lam)

            # Clip to prevent an unrealistic cluster of cars in a single second
            spawns[direction] = min(raw_spawn, self.max_spawn_per_step)

        return spawns