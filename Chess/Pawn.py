# import pygame as pg
from .Piece import Piece


class Pawn(Piece):
    def __init__(self, color, py, px):
        super().__init__('P', color, py, px)

        self.direction = -1 if color == 'white' else 1 # White pawn moves up and black ones down
        self.moved = 0                                 # If not moved then it could move two steps

    def get_possible_moves(self, board):
        all_possible_moves = set()

        one_step = board[self.py + self.direction][self.px]

        if not self.moved:
            two_step = board[self.py + self.direction * 2][self.px]

        left_attack = board[self.py + self.direction][self.px - 1] if self.px > 0 else None
        right_attack = board[self.py + self.direction][self.px + 1] if self.px < 7 else None

        if not one_step:
            all_possible_moves.add((self.py + self.direction, self.px))
            if not self.moved and not two_step:
                all_possible_moves.add((self.py + self.direction * 2, self.px))

        if right_attack and right_attack.color != self.color:
            all_possible_moves.add((self.py + self.direction, self.px + 1))

        if left_attack and left_attack.color != self.color:
            all_possible_moves.add((self.py + self.direction, self.px - 1))

        return all_possible_moves

    def move(self, board, dy, dx, reverse=False):
        if reverse:
            board[dy][dx] = self
            board[self.py][self.px] = 0

            self.px = dx
            self.py = dy

            self.moved -= 1

            return True

        all_possible_moves = set()

        one_step = board[self.py + self.direction][self.px]

        if not self.moved:
            two_step = board[self.py + self.direction * 2][self.px]

        left_attack = board[self.py + self.direction][self.px - 1] if self.px > 0 else None
        right_attack = board[self.py + self.direction][self.px + 1] if self.px < 7 else None

        if not one_step:
            all_possible_moves.add((self.px, self.py + self.direction ))
            if not self.moved and not two_step:
                all_possible_moves.add((self.px, self.py + self.direction * 2))

        if right_attack and right_attack.color != self.color:
            all_possible_moves.add((self.px + 1, self.py + self.direction))

        if left_attack and left_attack.color != self.color:
            all_possible_moves.add((self.px - 1, self.py + self.direction))

        if (dx, dy) in all_possible_moves:

            board[dy][dx] = self
            board[self.py][self.px] = 0

            self.px = dx
            self.py = dy

            self.moved += 1
            return True
        return False
