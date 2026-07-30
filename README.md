# RL Traffic Signal Optimizer
A modular traffic intersection simulator designed for Reinforcement Learning experiments.

The project aims to build an RL agent capable of learning optimal traffic signal control policies. Rather than relying on hardcoded traffic-light timings, the agent will learn from interaction with a realistic simulation environment.

## Project Goals
- Build a realistic four-way traffic intersection simulator.
- Support multiple reward functions for experimentation.
- Experiment with different reward functions and state representations.
- Train and compare algorithms such as SARSA, Q-Learning and Deep Q-Networks (DQN).
- Evaluate learned policies against fixed-time traffic signals.
- Analyze the impact of state encoding and reward design on RL performance.

## Current Features

### Vehicle Generation (env/vehicle_generator.py)
Vehicles arrive independently on each lane using a Poisson arrival process.
Each lane has its own configurable arrival rate (λ), allowing simulation of:
- Balanced traffic
- Rush-hour traffic
- Asymmetric traffic flow
To avoid unrealistic bursts, arrivals per timestep are capped at a configurable maximum.

### Traffic Signal Controller (env/environment.py)
The simulator models a standard four-way intersection with two traffic phases:
- North–South Green
- East–West Green

The environment supports two actions:
- KEEP – continue the current green phase
- SWITCH – change to the opposite phase
A configurable minimum green duration prevents unrealistic rapid switching.

### Queue-Based Traffic Model (env/environment.py) (env/car.py)
Each lane stores individual vehicle objects rather than simple counts.
Every vehicle records its entry time, allowing accurate computation of:
- Waiting time
- Queue length
- Vehicle throughput
- Remaining congestion
Vehicles move through the intersection whenever their direction receives a green signal.

### Configurable Reward Functions (env/reward_functions.py)
Reward functions are completely modular.
Current implementations include:
- Waiting Time Minimization
- Queue Length Minimization
- Throughput Reward
- Composite Reward (throughput + queue length + waiting time)
New reward functions can be added without modifying the environment. The desired reward is selected through config.py

### State Encoding (env/state_encoder.py)
~~For tabular RL methods, raw queue lengths are converted into discrete density buckets (to avoid state-space explosion):~~
| Queue Length | State |
| --- | --- |
| 0 | Empty |
| 1-3 | Low |
| 4-7 | Medium |
| 8-12 | High |
| >12 | Very High | 

NOTE: Current experiments investigate different state representations, including:
- Raw Queue-length counts
- Traffic density buckets


### Configurable Simulation (config.py)
Most simulation parameters are centralized in a configuration file, including:
- Lane capacity
- Episode length
- Minimum green duration
- Vehicle arrival rates
- Reward function selection

This allows experiments to be reproduced without modifying environment logic.

### Evaluation Framework

Policies are evaluated using several traffic performance metrics, including:
- Cumulative reward
- Average waiting time
- Vehicle throughput
- Vehicles departed
- Vehicles remaining
- Remaining cumulative waiting time
- Number of signal switches

A configurable Fixed-Time Controller is included as a baseline for comparison.

## Project Structure

```
Traffic-RL-Optimizer/
│
├── algorithms/
│   ├── fixed_time_agent.py      # Fixed-time baseline controller
│   └── sarsa_agent.py           # SARSA implementation
│
├── env/
│   ├── car.py                   # Vehicle model
│   ├── environment.py           # Traffic simulation environment
│   ├── reward_functions.py      # Modular reward functions
│   ├── state_encoder.py         # State representation for RL agents
│   └── vehicle_generator.py     # Poisson traffic generator
│
├── experiments/
│   ├── train_sarsa_agent.py         # Train SARSA agent
│   ├── evaluate_sarsa_agent.py      # Evaluate trained SARSA policy
│   └── evaluate_fixed_time_agent.py # Evaluate fixed-time baseline
│
├── q_tables/
│   └── sarsa_q_table.pkl        # Saved SARSA Q-table
│
├── config.py                    # Simulation and training configuration
├── debug.py                     # Debugging utilities
└── README.md
```

## Current Progress

✅ Four-way traffic simulation environment

✅ Poisson traffic generation

✅ Queue-based vehicle model

✅ Modular reward functions

✅ SARSA implementation

✅ Fixed-time baseline controller

✅ Evaluation framework

🔄 Q-Learning implementation

🔄 Expected SARSA implementation

🔄 Comparative performance analysis

🔄 Results Plotting

🔄 Visualizer
