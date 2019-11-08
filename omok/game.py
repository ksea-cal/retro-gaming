from sys import exit

import pygame

from omok.gomoku_ai import *
from omok.gomoku import *
from omok.render import GameRender


def play(params):
    gomoku = Gomoku(params)
    render = GameRender(gomoku, params)

    # AI settings
    agent = GomokuAI(gomoku, BoardState.BLACK, 2)
    second_agent = GomokuAI(gomoku, BoardState.WHITE, 1)

    result = BoardState.EMPTY

    # Assume AI agent plays first
    agent.first_step()
    result = gomoku.get_chess_result()
    render.change_state()

    while True:
        if params['enable_second_ai']:
            second_agent.one_step()
            result = gomoku.get_chess_result()
            if result != BoardState.EMPTY:
                print(result, "wins")
                break
            if params['enable_ai']:
                agent.one_step()
                result = gomoku.get_chess_result()
                if result != BoardState.EMPTY:
                    print(result, "wins")
                    break
            else:
                render.change_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if render.one_step():
                    result = gomoku.get_chess_result()
                else:
                    continue
                if result != BoardState.EMPTY:
                    break
                if params['enable_ai']:
                    agent.one_step()
                    result = gomoku.get_chess_result()
                else:
                    render.change_state()
        render.draw_chess()
        render.draw_mouse()

        if result != BoardState.EMPTY:
            render.draw_result(result)

        pygame.display.update()
