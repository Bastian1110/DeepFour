import gymnasium as gym
import numpy as np


class Connect4Env(gym.Env):
    def __init__(self):
        super(Connect4Env, self).__init__()
        self.board = np.zeros((6, 7), dtype=int)
        self.action_space = gym.spaces.Discrete(7)  # 7 columns to choose from
        self.observation_space = gym.spaces.Box(low=0, high=2, shape=(6, 7), dtype=int)
        self.current_player = 1  # Start with player 1

    def step(self, action):
        column = action
        row = self._drop_disc(column)
        if row is None:  # Invalid move
            return self._get_obs(), -10, False, False, {}

        done = self._check_for_win(row, column) or not np.any(
            self.board == 0
        )  # Check for win or draw

        reward = 1 if done else 0
        self.current_player = 3 - self.current_player  # Switch player
        return self._get_obs(), reward, done, False, {}

    def reset(self, seed=None, options=None):
        self.board.fill(0)
        self.current_player = 1
        return self._get_obs(), {}

    def _drop_disc(self, column):
        for row in range(5, -1, -1):
            if self.board[row, column] == 0:
                self.board[row, column] = self.current_player
                return row
        return None  # Invalid move

    def _check_for_win(self, row, column):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            for i in range(1, 4):
                r, c = row + dr * i, column + dc * i
                if (
                    0 <= r < 6
                    and 0 <= c < 7
                    and self.board[r, c] == self.current_player
                ):
                    count += 1
                else:
                    break
            for i in range(1, 4):
                r, c = row - dr * i, column - dc * i
                if (
                    0 <= r < 6
                    and 0 <= c < 7
                    and self.board[r, c] == self.current_player
                ):
                    count += 1
                else:
                    break
            if count >= 4:
                return True
        return False

    def _get_obs(self):
        return np.copy(self.board)

    def jsonify_game_state(self):
        return {"board": self.board.tolist()}
