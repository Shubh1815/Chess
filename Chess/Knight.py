# import pygame as pg
from .Piece import Piece


class Knight(Piece):
    def __init__(self, color, py, px):
        super().__init__('N', color, py, px)

    def get_possible_moves(self, board):
        i, j = self.py, self.px

        all_possible_moves = set()

        next_step = [
            (i + 2, j + 1),
            (i - 2, j - 1),
            (i - 1, j + 2),
            (i + 1, j - 2),

            (i + 2, j - 1),
            (i - 2, j + 1),
            (i + 1, j + 2),
            (i - 1, j - 2),
        ]

        for x, y in next_step:
            if 0 <= x < 8 and 0 <= y < 8 and (not board[x][y] or board[x][y].color != self.color):
                all_possible_moves.add((x, y))

        return all_possible_moves

    def move(self, board, dy, dx, reverse=False):
        if reverse:
            board[dy][dx] = self
            board[self.py][self.px] = 0

            self.px = dx
            self.py = dy
            return True

        i, j = self.py, self.px

        all_possible_moves = set()

        next_step = [
            (i + 2, j + 1),
            (i - 2, j - 1),
            (i - 1, j + 2),
            (i + 1, j - 2),

            (i + 2, j - 1),
            (i - 2, j + 1),
            (i + 1, j + 2),
            (i - 1, j - 2),
        ]

        for x, y in next_step:
            if 0 <= x < 8 and 0 <= y < 8 and (not board[x][y] or board[x][y].color != self.color):
                all_possible_moves.add((x, y))

        if (dy, dx) in all_possible_moves:
            board[dy][dx] = self
            board[self.py][self.px] = 0

            self.px = dx
            self.py = dy

            return True
        return False
