import random
import pygame
color = ['black', 'white']

piece_points = {
    '0': 0,
    'black-pawn': -10,
    'white-pawn': 10,
    'black-knight': -30,
    'white-knight': 30,
    'black-bishop': -30,
    'white-bishop': 30,
    'black-rook': -50,
    'white-rook': 50,
    'black-queen': -90,
    'white-queen': 90,
    'black-king': -1000,
    'white-king': 1000,
}

INF = float('inf')


def minmax(board, depth, alpha, beta):

    previous_turn = (depth + 1) & 1
    turn = depth & 1

    if board.game_over:
        if previous_turn:
            return -1500
        return 1500

    if not depth:
        return 0

    points = INF if turn else -INF

    for i in range(8):
        for j in range(8):
            if board.board[i][j] and board.board[i][j].color == color[turn]:
                next_moves = board.board[i][j].get_possible_moves(board.board)

                for ni, nj in list(next_moves):
                    captured_piece = board.board[ni][nj]
                    captured_points = piece_points[str(captured_piece)]

                    board.selected_piece = (i, j)
                    # board.board[i][j].select(j, i)
                    stop = False

                    if board.clicked(nj, ni, ai=True):
                        if not turn:
                            # Maximizing
                            points = max(points, minmax(board, depth - 1, alpha, beta) + captured_points + board.checked * 50)
                            alpha = max(alpha, points)
                            if alpha >= beta:
                                stop = True
                        else:
                            # Minimizing
                            points = min(points, minmax(board, depth - 1, alpha, beta) + captured_points - board.checked * 50)
                            beta = min(points, beta)
                            if beta <= alpha:
                                stop = True

                        board.checked = False
                        board.game_over = False

                        board.board[ni][nj].move(board.board, i, j, reverse=True)
                        board.board[ni][nj] = captured_piece

                        if stop:
                            return points

                    board.selected_piece = None
                    # board.board[i][j].select(j, i)

    return points


def get_best_move(game, turn):

    moves = {}

    board = game.board
    points = -INF

    piece = (-1, -1)
    next_move = (-1, -1)

    for i in range(8):
        for j in range(8):
            if board[i][j] and board[i][j].color == color[turn]:

                next_moves = board[i][j].get_possible_moves(board)

                for ni, nj in list(next_moves):
                    game.selected_piece = (i, j)
                    # board[i][j].select(j, i)

                    captured_piece = board[ni][nj]
                    captured_points = piece_points[str(captured_piece)]

                    if game.clicked(nj, ni, ai=True):
                        res_points = minmax(game, 3, -INF, INF) + captured_points + game.checked * 50

                        board[ni][nj].move(board, i, j, reverse=True)
                        board[ni][nj] = captured_piece

                        if res_points > points:
                            points = res_points
                            piece = (i, j)
                            next_move = (ni, nj)

                        game.checked = False
                        game.game_over = False

                    game.selected_piece = None
                    # board[i][j].select(j, i)

    board[piece[0]][piece[1]].select(piece[1], piece[0])
    game.selected_piece = piece
    return next_move
