# import pygame as pg
from .Piece import Piece


class Bishop(Piece):
    def __init__(self, color, py, px):
        super().__init__('B', color, py, px)

    def get_moves(self, board):
        return self.move_diagonal(board)
