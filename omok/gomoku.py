from omok.boardstate import *


class Gomoku:
    def __init__(self, params):
        self.params = params
        self._map = [
            [BoardState.EMPTY for j in range(self.params['board_size'])]
            for i in range(self.params['board_size'])
            ]
        self.current_i = -1
        self.current_j = -1
        self.curr_state = BoardState.EMPTY

    def get_map(self):
        return self._map

    def get_chessboard_state(self, i, j):
        return self._map[i][j]

    def set_chessboard_state(self, i, j, state):
        self._map[i][j] = state
        self.current_i = i
        self.current_j = j
        self.curr_state = state

    def get_chess_result(self):
        if self.connected_five(self.current_i, self.current_j, self.curr_state):
            return self.curr_state
        else:
            return BoardState.EMPTY

    def direction_count(self, i, j, x_dir, y_dir, player):
        count = 0
        # look four more steps on a certain direction
        for step in range(1, 5):
            if x_dir != 0 and (j + x_dir * step < 0 or j + x_dir * step >= self.params['board_size']):
                break
            if y_dir != 0 and (i + y_dir * step < 0 or i + y_dir * step >= self.params['board_size']):
                break
            if self._map[i + y_dir * step][j + x_dir * step] == player:
                count += 1
            else:
                break
        return count

    def connected_five(self, i, j, player):
        directions = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1), (1, -1)], [(-1, -1), (1, 1)]]
        for axis in directions:
            axis_count = 1
            for x_dir, y_dir in axis:
                axis_count += self.direction_count(i, j, x_dir, y_dir, player)
                if axis_count >= 5:
                    return True
        return False
