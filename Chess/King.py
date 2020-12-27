# import pygame as pg
from .Piece import Piece


class King(Piece):
    def __init__(self, color, py, px):
        super().__init__('K', color, py, px)

    def get_moves(self, board):
        """
        Returns the moves of all possible moves of king
        :param board: 8 X 8 Array
        :return: set of possible move
        """
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

    def check_pawn(self, board):
        """
        Checks if the king is attacked by opponent's pawn
        :param board: 8 X 8 Array
        :return: bool
        """
        i, j = self.py, self.px

        if self.color == 'w':
            try:
                if board[i - 1][j - 1].name == 'P' and board[i - 1][j - 1].color != self.color:
                    return True
            except (IndexError, AttributeError):
                pass

            try:
                if board[i - 1][j + 1].name == 'P' and board[i - 1][j + 1].color != self.color:
                    return True
            except (IndexError, AttributeError):
                pass
        else:
            try:
                if board[i + 1][j - 1].name == 'P' and board[i + 1][j - 1].color != self.color:
                    return True
            except (IndexError, AttributeError):
                pass

            try:
                if board[i + 1][j + 1].name == 'P' and board[i + 1][j + 1].color != self.color:
                    return True
            except (IndexError, AttributeError):
                pass

        return False

    def check_knight(self, board):
        """
        Checks if the king is attacked by opponent's Knight
        :param board: 8 X 8 Array
        :return: bool
        """

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
                if board[x][y].color != self.color and board[x][y].name == 'N':
                    return True
        return False

    def check_row_col(self, board):
        """
        Checks if the king is attacked by opponent's queen or rook
        :param board: 8 x 8 Array
        :return: bool
        """
        i = self.py
        l = r = self.px

        while l > 0:
            l -= 1
            if board[i][l]:
                if board[i][l].color != self.color:
                    if board[i][l].name in ('Q', 'R'):
                        return True
                    if abs(self.px - l) == 1 and board[i][l].name == 'K':
                        return True
                break

        while r < 7:
            r += 1
            if board[i][r]:
                if board[i][r].color != self.color:
                    if board[i][r].name in ('Q', 'R'):
                        return True
                    if abs(self.px - r) == 1 and board[i][r].name == 'K':
                        return True
                break

        u = d = self.py
        j = self.px

        while u > 0:
            u -= 1
            if board[u][j]:
                if board[u][j].color != self.color:
                    if board[u][j].name in ('Q', 'R'):
                        return True
                    if abs(self.py - u) == 1 and board[u][j].name == 'K':
                        return True
                break

        while d < 7:
            d += 1
            if board[d][j]:
                if board[d][j].color != self.color:
                    if board[d][j].name in ('Q', 'R'):
                        return True
                    if abs(self.py - d) == 1 and board[d][j].name == 'K':
                        return True
                break

        return False

    def check_diagonal(self, board):
        """
        Checks if the king is attacked by opponent's queen or bishop
        :param board:
        :return: bool
        """
        i, j = self.py, self.px

        # Upper Left
        while i > 0 and j > 0:
            i -= 1
            j -= 1
            if board[i][j]:
                if board[i][j].color != self.color:
                    if board[i][j].name in ('Q', 'B'):
                        return True
                    if abs(self.px - j) == abs(self.py - i) == 1 and board[i][j].name == 'K':
                        return True
                break

        i, j = self.py, self.px

        # Upper Right
        while i > 0 and j < 7:
            i -= 1
            j += 1
            if board[i][j]:
                if board[i][j].color != self.color:
                    if board[i][j].name in ('Q', 'B'):
                        return True
                    if abs(self.px - j) == abs(self.py - i) == 1 and board[i][j].name == 'K':
                        return True
                break

        i, j = self.py, self.px

        # Bottom Left
        while i < 7 and j > 0:
            i += 1
            j -= 1

            if board[i][j]:
                if board[i][j].color != self.color:
                    if board[i][j].name in ('Q', 'B'):
                        return True
                    if abs(self.px - j) == abs(self.py - i) == 1 and board[i][j].name == 'K':
                        return True
                break

        i, j = self.py, self.px

        # Bottom Right
        while i < 7 and j < 7:
            i += 1
            j += 1
            if board[i][j]:
                if board[i][j].color != self.color:
                    if board[i][j].name in ('Q', 'B'):
                        return True
                    if abs(self.px - j) == abs(self.py - i) == 1 and board[i][j].name == 'K':
                        return True
                break

        return False

    def is_check(self, board):
        """
        Checks if the king is attacked by any opponent's piece
        :param board: 8 x 8 Array
        :return: bool
        """

        if self.check_diagonal(board) or \
           self.check_row_col(board) or \
           self.check_knight(board) or \
           self.check_pawn(board):
            return True
        return False
