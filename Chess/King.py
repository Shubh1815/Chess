# import pygame as pg
from .Piece import Piece


class King(Piece):
    def __init__(self, color, py, px):
        super().__init__('K', color, py, px)

    def get_possible_moves(self, board):
        i, j = self.py, self.px
        all_possible_moves = set()

        next_step = [
            (i - 1, j),
            (i + 1, j),
            (i, j - 1),
            (i, j + 1),

            (i - 1, j - 1),
            (i - 1, j + 1),
            (i + 1, j - 1),
            (i + 1, j + 1),
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

        all_possible_moves = self.get_possible_moves(board)

        if (dy, dx) in all_possible_moves:

            new_place = board[dy][dx]
            prev_px, prev_py = self.px, self.py

            board[dy][dx] = self
            board[self.py][self.px] = 0

            self.px = dx
            self.py = dy

            # If moving to the new place does not give check to our king
            if not self.is_check(board):
                return True

            self.px = prev_px
            self.py = prev_py
            board[dy][dx] = new_place
            board[self.py][self.px] = self

        return False

    def check_pawn(self, board):

        i, j = self.py, self.px

        if self.color == 'white':
            try:
                if board[i - 1][j - 1].name == 'pawn' and board[i - 1][j - 1].color != self.color:
                    return True
            except (IndexError, AttributeError):
                pass

            try:
                if board[i - 1][j + 1].name == 'pawn' and board[i - 1][j + 1].color != self.color:
                    return True
            except (IndexError, AttributeError):
                pass
        else:
            try:
                if board[i + 1][j - 1].name == 'pawn' and board[i + 1][j - 1].color != self.color:
                    return True
            except (IndexError, AttributeError):
                pass

            try:
                if board[i + 1][j + 1].name == 'pawn' and board[i + 1][j + 1].color != self.color:
                    return True
            except (IndexError, AttributeError):
                pass

        return False

    def check_knight(self, board):

        i, j = self.py, self.px

        knight_steps = [
            (i + 2, j + 1),
            (i - 2, j - 1),
            (i - 1, j + 2),
            (i + 1, j - 2),

            (i + 2, j - 1),
            (i - 2, j + 1),
            (i + 1, j + 2),
            (i - 1, j - 2),
        ]

        for x, y in knight_steps:
            if 0 <= x < 8 and 0 <= y < 8 and board[x][y]:
                if board[x][y].color != self.color and board[x][y].name == 'knight':
                    return True
        return False

    def check_row_col(self, board):
        i = self.py
        l = r = self.px

        while l > 0:
            l -= 1
            if board[i][l]:
                if board[i][l].color != self.color:
                    if board[i][l].name in ('queen', 'rook'):
                        return True
                    if abs(self.px - l) == 1 and board[i][l].name == 'king':
                        return True
                break

        while r < 7:
            r += 1
            if board[i][r]:
                if board[i][r].color != self.color:
                    if board[i][r].name in ('queen', 'rook'):
                        return True
                    if abs(self.px - r) == 1 and board[i][r].name == 'king':
                        return True
                break

        u = d = self.py
        j = self.px

        while u > 0:
            u -= 1
            if board[u][j]:
                if board[u][j].color != self.color:
                    if board[u][j].name in ('queen', 'rook'):
                        return True
                    if abs(self.py - u) == 1 and board[u][j].name == 'king':
                        return True
                break

        while d < 7:
            d += 1
            if board[d][j]:
                if board[d][j].color != self.color:
                    if board[d][j].name in ('queen', 'rook'):
                        return True
                    if abs(self.py - d) == 1 and board[d][j].name == 'king':
                        return True
                break

        return False

    def check_diagonal(self, board):
        i, j = self.py, self.px

        # Upper Left
        while i > 0 and j > 0:
            i -= 1
            j -= 1
            if board[i][j]:
                if board[i][j].color != self.color:
                    if board[i][j].name in ('queen', 'bishop'):
                        return True
                    if abs(self.px - j) == abs(self.py - i) == 1 and board[i][j].name == 'king':
                        return True
                break

        i, j = self.py, self.px

        # Upper Right
        while i > 0 and j < 7:
            i -= 1
            j += 1
            if board[i][j]:
                if board[i][j].color != self.color:
                    if board[i][j].name in ('queen', 'bishop'):
                        return True
                    if abs(self.px - j) == abs(self.py - i) == 1 and board[i][j].name == 'king':
                        return True
                break

        i, j = self.py, self.px

        # Bottom Left
        while i < 7 and j > 0:
            i += 1
            j -= 1

            if board[i][j]:
                if board[i][j].color != self.color:
                    if board[i][j].name in ('queen', 'bishop'):
                        return True
                    if abs(self.px - j) == abs(self.py - i) == 1 and board[i][j].name == 'king':
                        return True
                break

        i, j = self.py, self.px

        # Bottom Right
        while i < 7 and j < 7:
            i += 1
            j += 1
            if board[i][j]:
                if board[i][j].color != self.color:
                    if board[i][j].name in ('queen', 'bishop'):
                        return True
                    if abs(self.px - j) == abs(self.py - i) == 1 and board[i][j].name == 'king':
                        return True
                break

        return False

    def is_check(self, board):

        if self.check_diagonal(board) or \
           self.check_row_col(board) or \
           self.check_knight(board) or \
           self.check_pawn(board):
            return True
        return False
