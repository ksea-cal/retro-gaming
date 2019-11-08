import pygame
from omok.boardstate import *

IMAGE_PATH = 'img/'
WIDTH = 540
HEIGHT = 540
MARGIN = 22
PIECE = 32


class GameRender:
    def __init__(self, gomoku, params):
        self.params = params
        self.GRID = (WIDTH - 2 * MARGIN) / (self.params['board_size'] - 1)
        self._gomoku = gomoku
        self.curr_piece_state = BoardState.BLACK
        pygame.init()
        self._screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        pygame.display.set_caption('AI for Gomoku')
        self._ui_chessboard = pygame.image.load(IMAGE_PATH + 'chessboard.jpg').convert()
        self._ui_piece_black = pygame.image.load(IMAGE_PATH + 'piece_black.png').convert_alpha()
        self._ui_piece_white = pygame.image.load(IMAGE_PATH + 'piece_white.png').convert_alpha()

    def coordinate_transform_map2pixel(self, i, j):
        return MARGIN + j * self.GRID - PIECE / 2, MARGIN + i * self.GRID - PIECE / 2

    def coordinate_transform_pixel2map(self, x, y):
        i, j = int((y - MARGIN + PIECE / 2) / self.GRID), int((x - MARGIN + PIECE / 2) / self.GRID)
        if i < 0 or i >= self.params['board_size'] or j < 0 or j >= self.params['board_size']:
            return None, None
        else:
            return i, j

    def draw_chess(self):
        self._screen.blit(self._ui_chessboard, (0, 0))
        for i in range(0, self.params['board_size']):
            for j in range(0, self.params['board_size']):
                x, y = self.coordinate_transform_map2pixel(i, j)
                state = self._gomoku.get_chessboard_state(i, j)
                if state == BoardState.BLACK:
                    self._screen.blit(self._ui_piece_black, (x, y))
                elif state == BoardState.WHITE:
                    self._screen.blit(self._ui_piece_white, (x, y))
                else:
                    pass

    def draw_mouse(self):
        x, y = pygame.mouse.get_pos()
        if self.curr_piece_state == BoardState.BLACK:
            self._screen.blit(self._ui_piece_black, (x - PIECE / 2, y - PIECE / 2))
        else:
            self._screen.blit(self._ui_piece_white, (x - PIECE / 2, y - PIECE / 2))

    def draw_result(self, result):
        font = pygame.font.SysFont('Arial', 55)
        tips = 'Game Over:'
        if result == BoardState.BLACK:
            tips = tips + 'Black Wins'
        elif result == BoardState.WHITE:
            tips = tips + 'White Wins'
        else:
            tips = tips + 'Draw'
        text = font.render(tips, True, (0, 0, 255))
        self._screen.blit(text, (WIDTH / 2 - 200, HEIGHT / 2 - 50))

    def one_step(self):
        i, j = None, None
        mouse_button = pygame.mouse.get_pressed()
        if mouse_button[0]:
            x, y = pygame.mouse.get_pos()
            i, j = self.coordinate_transform_pixel2map(x, y)
        if i is not None and j is not None:
            if self._gomoku.get_chessboard_state(i, j) != BoardState.EMPTY:
                return False
            else:
                self._gomoku.set_chessboard_state(i, j, self.curr_piece_state)
                return True
        return False

    def change_state(self):
        if self.curr_piece_state == BoardState.BLACK:
            self.curr_piece_state = BoardState.WHITE
        else:
            self.curr_piece_state = BoardState.BLACK
