# import pygame as pg
from .Piece import Piece


class Queen(Piece):
    def __init__(self, color, py, px):
        super().__init__('Q', color, py, px)

    def get_moves(self, board):
        all_possible_moves = self.move_diagonal(board)
        all_possible_moves = all_possible_moves.union(self.move_row(board))
        all_possible_moves = all_possible_moves.union(self.move_col(board))

        return all_possible_moves
