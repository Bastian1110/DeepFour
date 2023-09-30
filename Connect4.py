import gymnasium as gym
import numpy as np


class Connect4Env(gym.Env):
    def __init__(self):
        super(Connect4Env, self).__init__()
        self.board = np.zeros((6, 7), dtype=int)
        self.action_space = gym.spaces.Discrete(7)  # 7 columns to choose from
        self.observation_space = gym.spaces.Box(low=0, high=2, shape=(6, 7), dtype=int)
        self.current_player = 1  # Start with player 1
        self.players_moves = {1: 0, 2: 0}

    def step(self, action):
        column = action
        row = self._drop_disc(column)
        info = (
            {"action": action}
            if isinstance(action, int)
            else {"action": action.tolist()}
        )

        if row is None:  # Invalid move
            return self._get_obs(), -10, False, False, info

        self.players_moves[self.current_player] += 1

        reward = 0.1

        # If conect with own pieces
        reward = reward + (
            self.count_connected_pieces(self.current_player, row, column) * 0.2
        )

        done = self._check_for_win(self.current_player, row, column) or not np.any(
            self.board == 0
        )

        if not done:
            # Let oponent win
            for col in range(7):
                next_row = self._drop_disc(col, put_piece=False)
                if next_row is not None and self._check_for_win(
                    self.get_next_player(self.current_player), next_row, col
                ):
                    reward = -10

            # Check if blocked win of openent
            if self._check_for_win(
                self.get_next_player(self.current_player), row, column
            ):
                reward = 8
        else:
            if self._check_for_win(self.current_player, row, column):
                reward = 12 + ((30 - self.players_moves[self.current_player]) * 0.25)

        self.current_player = 3 - self.current_player
        return self._get_obs(), reward, done, False, info

    def reset(self, seed=None, options=None):
        self.board.fill(0)
        self.current_player = 1
        self.players_moves = {1: 0, 2: 0}
        return self._get_obs(), {}

    def get_next_player(self, player):
        if player == 1:
            return 2
        else:
            return 1

    def count_connected_pieces(self, player, row, col):
        connected_count = 0
        directions = [
            (-1, 0),  # Up
            (1, 0),  # Down
            (0, -1),  # Left
            (0, 1),  # Right
            (-1, -1),  # Up-Left
            (-1, 1),  # Up-Right
            (1, -1),  # Down-Left
            (1, 1),  # Down-Right
        ]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if (
                0 <= r < len(self.board)
                and 0 <= c < len(self.board[0])
                and self.board[r][c] == player
            ):
                connected_count += 1

        return connected_count

    def _drop_disc(self, column, put_piece=True):
        for row in range(5, -1, -1):
            if self.board[row, column] == 0:
                if put_piece:
                    self.board[row, column] = self.current_player
                return row
        return None  # Invalid move

    def _check_for_win(self, player, row, column):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            for i in range(1, 4):
                r, c = row + dr * i, column + dc * i
                if 0 <= r < 6 and 0 <= c < 7 and self.board[r, c] == player:
                    count += 1
                else:
                    break
            for i in range(1, 4):
                r, c = row - dr * i, column - dc * i
                if 0 <= r < 6 and 0 <= c < 7 and self.board[r, c] == player:
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
