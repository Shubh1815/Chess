import os
from collections import deque
from .King import King
from .Queen import Queen
from .Bishop import Bishop
from .Knight import Knight
from .Rook import Rook
from .Pawn import Pawn


class Board:
    def __init__(self):
        self.board = [
            [
                Rook('b', 0, 0),
                Knight('b', 0, 1),
                Bishop('b', 0, 2),
                Queen('b', 0, 3),
                King('b', 0, 4),
                Bishop('b', 0, 5),
                Knight('b', 0, 6),
                Rook('b', 0, 7),
            ],
            [
                Pawn('b', 1, 0),
                Pawn('b', 1, 1),
                Pawn('b', 1, 2),
                Pawn('b', 1, 3),
                Pawn('b', 1, 4),
                Pawn('b', 1, 5),
                Pawn('b', 1, 6),
                Pawn('b', 1, 7)
            ],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [
                Pawn('w', 6, 0),
                Pawn('w', 6, 1),
                Pawn('w', 6, 2),
                Pawn('w', 6, 3),
                Pawn('w', 6, 4),
                Pawn('w', 6, 5),
                Pawn('w', 6, 6),
                Pawn('w', 6, 7)
            ],
            [
                Rook('w', 7, 0),
                Knight('w', 7, 1),
                Bishop('w', 7, 2),
                Queen('w', 7, 3),
                King('w', 7, 4),
                Bishop('w', 7, 5),
                Knight('w', 7, 6),
                Rook('w', 7, 7),
            ],
        ]

        self.selected = None  # Stores Selected piece

        self.turn = 1  # 1 means its white's turn

        self.king = [self.board[0][4], self.board[7][4]]  # To check for "Checks" after every move

        self.check = False
        self.check_mate = False
        self.game_over = False

        self.history = deque([], 5)

        self.black_time_elapsed = 0
        self.white_time_elapsed = 0

    def get_moves(self, color):
        """
        Returns a dict of all moves possible of pieces of given color
        :param color: 'b' or 'w' (str)
        :return: dictionary of all moves for given color
        """

        possible_moves = dict()

        for i in range(8):
            for j in range(8):
                if self.board[i][j] and self.board[i][j].color == color:
                    possible_moves[(i, j)] = self.board[i][j].get_moves(self.board)

        return possible_moves

    def select(self, mx, my):
        """
        Select a current player's piece
        If a piece is already selected then move the selected piece to (my, mx) by calling move method
        :param mx: int
        :param my: int
        :return: None
        """
        if not self.is_in_bounds(mx, my) or self.game_over:
            return

        if not self.selected or self.selected == (my, mx):
            if self.is_player_piece((my, mx)):
                self.board[my][mx].select()
                if self.board[my][mx].selected:
                    self.selected = (my, mx)
                else:
                    self.selected = None
        else:
            if self.is_move_possible(self.selected, (my, mx)):

                self.move(self.selected, (my, mx))
                # self.print_board()

                # Unselect the moved piece
                self.board[my][mx].select()
                self.selected = None

    def is_move_possible(self, source, dest):
        """
        Check if possible to move piece from source to dest
        :param source: Coordinates of source piece (int, int)
        :param dest: Coordinates of dest piece (int, int)
        :return: bool
        """
        sy, sx = source
        dy, dx = dest

        source_piece = self.board[sy][sx]
        dest_piece = self.board[dy][dx]

        moves = self.board[sy][sx].get_moves(self.board)

        if (dy, dx) not in moves:
            return False

        source_piece.move_position(dx, dy)
        self.board[dy][dx], self.board[sy][sx] = source_piece, None

        is_valid_move = True
        if self.in_check(self.turn):
            is_valid_move = False

        source_piece.move_position(sx, sy)
        self.board[dy][dx], self.board[sy][sx] = dest_piece, source_piece

        return is_valid_move

    def move(self, source, dest, history=True):
        """
        Moves a piece from source to dest
        :param source: Coordinates of source piece (int, int)
        :param dest: Coordinates of dest piece (int, int)
        :param history: Whether to add this move to history (bool)
        :return: Captured Piece
        """

        self.check = False

        sy, sx = source
        dy, dx = dest

        source_piece = self.board[sy][sx]
        dest_piece = self.board[dy][dx]

        source_piece.move_position(dx, dy)
        self.board[dy][dx], self.board[sy][sx] = source_piece, None

        if history:
            self.history.append((self.turn, source, dest))

        self.turn ^= 1

        if self.in_check(self.turn):
            self.check = True
            if self.in_checkmate():
                self.check_mate = True
                self.game_over = True

        return dest_piece

    def is_player_piece(self, square):
        """
        Checks if the square contains the current player's piece
        :param square: Coordinates for the piece (int, int)
        :return: bool
        """
        my, mx = square

        if not self.board[my][mx]:
            return False

        color = ['b', 'w']

        return color[self.turn] == self.board[my][mx].color

    def in_check(self, turn):
        """
        Checks if the given turn's king is in check
        :param turn: 1 or 0 (int)
        :return: bool
        """

        return self.king[turn].is_check(self.board)

    def in_checkmate(self):
        """
        Checks if the the opponent's king is in checkmate after current move
        :return: bool
        """
        color = ['b', 'w']

        moves = self.get_moves(color[self.turn])
        for sy, sx in moves:
            source_piece = self.board[sy][sx]
            for dy, dx in moves[(sy, sx)]:
                valid_move = False
                dest_piece = self.board[dy][dx]

                source_piece.move_position(dx, dy)
                self.board[dy][dx], self.board[sy][sx] = source_piece, None

                if not self.in_check(self.turn):
                    valid_move = True

                source_piece.move_position(sx, sy)
                self.board[dy][dx], self.board[sy][sx] = dest_piece, source_piece

                if valid_move:
                    return False

        return True

    def print_board(self):
        """
        Prints the board to the console
        :return: None
        """

        os.system('clear')

        for i in range(8):
            print(("-" * 39))
            for j in range(8):
                print(self.board[i][j] if self.board[i][j] else '  ', end=" | ")
            print()
        print(("-" * 39))
        print('\n')

    @staticmethod
    def is_in_bounds(mx, my):
        """
        Checks if the coordinates are in bounds.
        :param mx: int
        :param my: int
        :return: bool
        """
        return 0 <= mx < 8 and 0 <= my <= 8
