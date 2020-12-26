# import pygame as pg
from .Piece import Piece


class Bishop(Piece):
    def __init__(self, color, py, px):
        super().__init__('B', color, py, px)

    def get_possible_moves(self, board):
        return self.move_diagonal(board)

    def move(self, board, dy, dx, reverse=False):
        if reverse:
            board[dy][dx] = self
            board[self.py][self.px] = 0

            self.px = dx
            self.py = dy

            return True

        all_possible_moves = self.move_diagonal(board)

        if (dy, dx) in all_possible_moves:

            board[dy][dx] = self
            board[self.py][self.px] = 0

            self.px = dx
            self.py = dy
            return True
        return False
