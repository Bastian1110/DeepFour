import gymnasium as gym
from gymnasium import spaces


class Connect4(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self, render_mode=None) -> None:
        self.action_space = spaces.Discrete(6)
