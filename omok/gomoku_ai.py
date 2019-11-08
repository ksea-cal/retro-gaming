from copy import deepcopy

from omok.evaluate import *


class GomokuAI:
    def __init__(self, gomoku, curr_state, depth):
        self.gomoku = gomoku
        self._curr_state = curr_state
        self._depth = depth
        self._curr_i = -1
        self._curr_j = -1

    def set_board(self, i, j, state):
        self.gomoku.set_chessboard_state(i, j, state)

    def has_neighbor(self, i, j):
        """
        Returns True if a specific point on the board has neighbors.
        Def [Neighbors] pieces within 2 empty intersections.
        :param i: x-axis
        :param j: y-axis
        :return: Boolean, True if (i, j) has neighbors
        """
        # exhaustive search for four axes
        directions = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1), (1, -1)], [(-1, -1), (1, 1)]]
        for axis in directions:
            for x_dir, y_dir in axis:
                if (x_dir != 0 and (j + x_dir < 0 or j + x_dir >= self.gomoku.hparams['board_size'])) \
                        or (y_dir != 0 and (i + y_dir < 0 or i + y_dir >= self.gomoku.hparams['board_size']))\
                        or (x_dir != 0 and (j + x_dir * 2 < 0 or j + x_dir * 2 >= self.gomoku.hparams['board_size']))\
                        or (y_dir != 0 and (i + y_dir * 2 < 0 or i + y_dir * 2 >= self.gomoku.hparams['board_size'])):
                    break
                m = self.gomoku.get_map()
                if m[i + y_dir][j + x_dir] != BoardState.EMPTY or m[i + y_dir * 2][j + x_dir * 2] != BoardState.EMPTY:
                    return True
        return False

    def direction_count(self, i, j, x_dir, y_dir, state):
        """
        Counts how many connected pieces are in a specific direction.
        :return: Integer, number of connected pieces in the desired direction
        """
        count = 0
        for step in range(1, 5):  # look four more steps on a certain direction
            if x_dir != 0 and (j + x_dir * step < 0 or j + x_dir * step >= self.gomoku.hparams['board_size']):
                break
            if y_dir != 0 and (i + y_dir * step < 0 or i + y_dir * step >= self.gomoku.hparams['board_size']):
                break
            if self.gomoku.get_map()[i + y_dir * step][j + x_dir * step] == state:
                count += 1
            else:
                break
        return count

    def direction_pattern(self, i, j, xdirection, ydirection, state):
        '''
        Returns the pattern with length 6 to evaluate later
        '''

        pattern = []
        for step in range(-1, 5):  # generate a list with len 10
            if xdirection != 0 and (j + xdirection * step < 0 or j + xdirection * step >= self.gomoku.hparams['board_size']):
                break
            if ydirection != 0 and (i + ydirection * step < 0 or i + ydirection * step >= self.gomoku.hparams['board_size']):
                break

            pattern.append(self.gomoku.get_map()[i + ydirection * step][j + xdirection * step])

        return pattern

    def has_checkmate(self, state, i, j):
        '''
        Checkmate means five in a row.
        '''
        directions = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1), (1, -1)], [(-1, -1), (1, 1)]]

        for axis in directions:
            axis_count = 1
            for (xdirection, ydirection) in axis:
                axis_count += self.direction_count(i, j, xdirection, ydirection, state)
                if axis_count >= 5:
                    return True
        return False

    def has_check(self, state, i, j):
        '''
        Check means a unblocked four.
        Double-three should also be a check, but it's not added yet.
        '''
        directions = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1), (1, -1)], [(-1, -1), (1, 1)]]

        for axis in directions:
            currentPattern = []
            for (xdirection, ydirection) in axis:
                currentPattern += self.direction_pattern(i, j, xdirection, ydirection, state)
                if len(currentPattern) > 2:
                    currentPattern[1] = state
                if enum_to_string(currentPattern) == WHITE_6PATTERNS[0]:
                    return True
                if enum_to_string(currentPattern) == BLACK_6PATTERNS[0]:
                    return True
        return False

    def opponent_has_checkmate(self, state):
        '''
        Check if opponent has checkmate.
        '''
        vectors = []

        # exhaustive search

        for i in range(self.gomoku.hparams['board_size']):
            vectors.append(self.gomoku.get_map()[i])

        for j in range(self.gomoku.hparams['board_size']):
            vectors.append([self.gomoku.get_map()[i][j] for i in range(self.gomoku.hparams['board_size'])])

        vectors.append([self.gomoku.get_map()[x][x] for x in range(self.gomoku.hparams['board_size'])])
        for i in range(1, self.gomoku.hparams['board_size'] - 4):
            v = [self.gomoku.get_map()[x][x - i] for x in range(i, self.gomoku.hparams['board_size'])]
            vectors.append(v)
            v = [self.gomoku.get_map()[y - i][y] for y in range(i, self.gomoku.hparams['board_size'])]
            vectors.append(v)

        vectors.append([self.gomoku.get_map()[x][self.gomoku.hparams['board_size'] - x - 1] for x in range(self.gomoku.hparams['board_size'])])
        for i in range(4, self.gomoku.hparams['board_size'] - 1):
            v = [self.gomoku.get_map()[x][i - x] for x in range(i, -1, -1)]
            vectors.append(v)
            v = [self.gomoku.get_map()[x][self.gomoku.hparams['board_size'] - x + self.gomoku.hparams['board_size'] - i - 2] for x in range(self.gomoku.hparams['board_size'] - i - 1, self.gomoku.hparams['board_size'])]
            vectors.append(v)

        # checkmate
        for vector in vectors:
            temp = enum_to_string(vector)
            if state == BoardState.BLACK:
                for pattern in WHITE_5PATTERNS:
                    if sublist(pattern, temp):
                        return True
            if state == BoardState.WHITE:
                for pattern in BLACK_5PATTERNS:
                    if sublist(pattern, temp):
                        return True
        return False

    def generate(self):
        '''
        Generate a list of available points for searching.
        '''
        frontierList = []
        for i in range(self.gomoku.hparams['board_size']):
            for j in range(self.gomoku.hparams['board_size']):
                if self.gomoku.get_map()[i][j] != BoardState.EMPTY:
                    continue  # only search for available spots
                if not self.has_neighbor(self.gomoku.get_map()[i][j], i, j):
                    continue

                if self._curr_state == BoardState.WHITE:
                    nextState = BoardState.BLACK
                else:
                    nextState = BoardState.WHITE

                # depth -1 every time
                nextPlay = GomokuAI(deepcopy(self.gomoku), nextState, self._depth - 1)
                nextPlay.set_board(i, j, self._curr_state)

                frontierList.append((nextPlay, i, j))

        # Degree Heuristcs, Sort points based on their evaluation

        frontierScores = []
        for node in frontierList:
            frontierScores.append(self.evaluate_point(node[1], node[2]))

        frontierZipped = zip(frontierList, frontierScores)
        frontierSorted = sorted(frontierZipped, key=lambda t: t[1])
        (frontierList, frontierScores) = zip(*frontierSorted)
        return frontierList

    def negate(self):
        return -self.evaluate()

    def evaluate(self):
        '''
        Return the board score for Minimax Search.
        '''
        # exhaustive search
        vectors = []

        for i in range(self.gomoku.hparams['board_size']):
            vectors.append(self.gomoku.get_map()[i])

        for j in range(self.gomoku.hparams['board_size']):
            vectors.append([self.gomoku.get_map()[i][j] for i in range(self.gomoku.hparams['board_size'])])

        vectors.append([self.gomoku.get_map()[x][x] for x in range(self.gomoku.hparams['board_size'])])
        for i in range(1, self.gomoku.hparams['board_size'] - 4):
            v = [self.gomoku.get_map()[x][x - i] for x in range(i, self.gomoku.hparams['board_size'])]
            vectors.append(v)
            v = [self.gomoku.get_map()[y - i][y] for y in range(i, self.gomoku.hparams['board_size'])]
            vectors.append(v)

        vectors.append([self.gomoku.get_map()[x][self.gomoku.hparams['board_size'] - x - 1] for x in range(self.gomoku.hparams['board_size'])])

        for i in range(4, self.gomoku.hparams['board_size'] - 1):
            v = [self.gomoku.get_map()[x][i - x] for x in range(i, -1, -1)]
            vectors.append(v)
            v = [self.gomoku.get_map()[x][self.gomoku.hparams['board_size'] - x + self.gomoku.hparams['board_size'] - i - 2] for x in range(self.gomoku.hparams['board_size'] - i - 1, self.gomoku.hparams['board_size'])]
            vectors.append(v)

        board_score = 0

        for v in vectors:
            score = evaluate_vector(v)
            if self._curr_state == BoardState.WHITE:
                board_score += score['black'] - score['white']
            else:
                board_score += score['white'] - score['black']
        return board_score

    def evaluate_point(self, i, j):
        '''
        Return a point score for Degree Heuristics.
        '''
        vectors = []
        vectors.append(self.gomoku.get_map()[i])
        vectors.append([self.gomoku.get_map()[i][j] for i in range(self.gomoku.hparams['board_size'])])

        if j > i:
            v = [self.gomoku.get_map()[x][x + j - i] for x in range(0, self.gomoku.hparams['board_size'] - j + i)]
            vectors.append(v)
        elif j == i:

            vectors.append([self.gomoku.get_map()[x][x] for x in range(self.gomoku.hparams['board_size'])])
        elif j < i:

            v = [self.gomoku.get_map()[x + i - j][x] for x in range(0, self.gomoku.hparams['board_size'] - i + j)]
            vectors.append(v)

        if i + j == self.gomoku.hparams['board_size'] - 1:
            vectors.append([self.gomoku.get_map()[x][self.gomoku.hparams['board_size'] - 1 - x] for x in range(self.gomoku.hparams['board_size'])])
        elif i + j < self.gomoku.hparams['board_size'] - 1:

            v = [self.gomoku.get_map()[x][self.gomoku.hparams['board_size'] - 1 - x - abs(i - j)] for x in range(self.gomoku.hparams['board_size'] - abs(i - j))]
            vectors.append(v)
        elif i + j > self.gomoku.hparams['board_size'] - 1:

            vectors.append(
                [self.gomoku.get_map()[x][self.gomoku.hparams['board_size'] - 1 - x + i + j - self.gomoku.hparams['board_size'] + 1] for x in range(i + j - self.gomoku.hparams['board_size'] + 1, self.gomoku.hparams['board_size'])])

        point_score = 0
        for v in vectors:
            score = evaluate_vector(v)
            if self._curr_state == BoardState.WHITE:
                point_score += score['white']
            else:
                point_score += score['black']
        return point_score

    def alpha_beta_prune(self, ai, alpha=-10000000, beta=10000000):

        if ai._depth <= 0:
            score = ai.negate()
            return score

        # only use the first 20 nodes

        # for (nextPlay, i, j) in ai.generate()[:20]:
        for (nextPlay, i, j) in ai.generate():
            temp_score = -self.alpha_beta_prune(nextPlay, -beta, -alpha)
            if temp_score > beta:
                return beta
            if temp_score > alpha:
                alpha = temp_score
                (ai._currentI, ai._currentJ) = (i, j)
        return alpha

    def first_step(self):
        # AI plays in the center
        self.gomoku.set_chessboard_state(7, 7, self._curr_state)
        return True

    def one_step(self):
        for i in range(self.gomoku.hparams['board_size']):
            for j in range(self.gomoku.hparams['board_size']):
                if self.gomoku.get_map()[i][j] != BoardState.EMPTY:
                    continue  # only search for available spots

                if self.has_checkmate(self._curr_state, i, j):
                    print('has checkmate')
                    self.gomoku.set_chessboard_state(i, j, self._curr_state)
                    return True

                if not self.has_neighbor(self.gomoku.get_map()[i][j], i, j):
                    continue

                if self.has_check(self._curr_state, i, j):
                    print
                    'has check, checking if opponent already has one...'

                    if self.opponent_has_checkmate(self._curr_state) is True:

                        print('not safe, searching other moves...')
                    elif self.opponent_has_checkmate(self._curr_state) is False:

                        print('safe')
                        self.gomoku.set_chessboard_state(i, j, self._curr_state)
                        return True

        node = GomokuAI(self.gomoku, self._curr_state, self._depth)
        score = self.alpha_beta_prune(node)
        print(score)
        (i, j) = (node._curr_i, node._curr_j)

        if not i is None and not j is None:
            if self.gomoku.get_chessboard_state(i, j) != BoardState.EMPTY:
                self.one_step()
            else:
                self.gomoku.set_chessboard_state(i, j, self._curr_state)
                return True
        return False
