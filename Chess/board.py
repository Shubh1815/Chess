# import pygame as pg
from .King import King
from .Queen import Queen
from .Bishop import Bishop
from .Knight import Knight
from .Rook import Rook
from .Pawn import Pawn
from .Ai import get_best_move
from utils import Label


class Board:
    def __init__(self, width, height):
        self.board = [
            [
                Rook('black', 0, 0),
                Knight('black', 0, 1),
                Bishop('black', 0, 2),
                Queen('black', 0, 3),
                King('black', 0, 4),
                Bishop('black', 0, 5),
                Knight('black', 0, 6),
                Rook('black', 0, 7),
            ],
            [
                Pawn('black', 1, 0),
                Pawn('black', 1, 1),
                Pawn('black', 1, 2),
                Pawn('black', 1, 3),
                Pawn('black', 1, 4),
                Pawn('black', 1, 5),
                Pawn('black', 1, 6),
                Pawn('black', 1, 7)
            ],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [
                Pawn('white', 6, 0),
                Pawn('white', 6, 1),
                Pawn('white', 6, 2),
                Pawn('white', 6, 3),
                Pawn('white', 6, 4),
                Pawn('white', 6, 5),
                Pawn('white', 6, 6),
                Pawn('white', 6, 7)
            ],
            [
                Rook('white', 7, 0),
                Knight('white', 7, 1),
                Bishop('white', 7, 2),
                Queen('white', 7, 3),
                King('white', 7, 4),
                Bishop('white', 7, 5),
                Knight('white', 7, 6),
                Rook('white', 7, 7),
            ],
        ]

        self.block_width = width // 8
        self.block_height = height // 8

        self.selected_piece = None

        # 1 means its white's turn
        self.turn = 1

        # To check for "Checks" after every move
        self.king = [self.board[0][4], self.board[7][4]]

        self.checked = False
        self.game_over = False

        self.message = Label('')
        self.message_victory = Label('')
        self.message_victory.config(color=(255, 255, 255), font_size=32)
        self.message.config(color=(255, 255, 255), font_size=48)

    def clicked(self, mx, my, ai=False):

        if self.game_over:
            return False

        color = ['black', 'white']

        if not ai:
            j, i = mx // 85, my // 85
        else:
            j, i = mx, my

        if self.selected_piece is None and not ai:
            if not self.board[i][j]:
                return False

            if self.board[i][j].color == color[self.turn]:
                self.board[i][j].select(j, i)

                if self.board[i][j].selected:
                    self.selected_piece = (i, j)
                else:
                    self.selected_piece = None
            return True
        else:
            si, sj = self.selected_piece
            # print(self.board[si][sj])
            # Storing the selected spot, if illegal move happens than revert back
            selected_spot = self.board[i][j]

            self.selected_piece = None
            self.board[si][sj].select(j, i)  # unselect the selected piece

            if self.checked:
                if self.board[si][sj].move(self.board, i, j):
                    # If this moves counter's Check, then perform it else revert back
                    if not self.king[self.turn].is_check(self.board):
                        self.turn ^= 1
                        self.message.change_text('')
                        self.checked = False

                        return True
                    else:
                        self.board[i][j].move(self.board, si, sj, reverse=True)
                        self.board[i][j] = selected_spot

            else:
                if self.board[si][sj].move(self.board, i, j):
                    # If the current moves doesn't give check to our king, then perform it else revert back
                    if not self.king[self.turn].is_check(self.board):
                        self.turn ^= 1
                        self.message.change_text('')
                        self.message_victory.change_text('')
                        # Check if this move gives check to opponent's king
                        if self.king[self.turn].is_check(self.board):
                            self.checked = True
                            # If checkmate then game over else continue
                            if self.is_checkmate():
                                # print('Checkmate')
                                self.message.change_text('Checkmate')
                                self.message_victory.change_text(f'{color[self.turn ^ 1].capitalize()} Wins')
                                self.game_over = True

                            self.message.change_text('Check')
                        return True
                    else:
                        self.board[i][j].move(self.board, si, sj, reverse=True)
                        self.board[i][j] = selected_spot
            return False

    def is_checkmate(self):
        # Make It more efficient

        # If either of the king is not checked then simply return else check for checkmate
        if not self.checked:
            return

        color = ['black', 'white']

        for i in range(8):
            for j in range(8):
                # For every defending piece check if it could counter check
                if self.board[i][j] and self.board[i][j].color == color[self.turn]:
                    all_moves = list(self.board[i][j].get_possible_moves(self.board))

                    for x, y in all_moves:
                        selected_spot = self.board[x][y]

                        if self.board[i][j].move(self.board, x, y):
                            if not self.king[self.turn].is_check(self.board):
                                self.board[x][y].move(self.board, i, j, reverse=True)
                                self.board[x][y] = selected_spot
                                return False

                            self.board[x][y].move(self.board, i, j, reverse=True)
                            self.board[x][y] = selected_spot
        return True

    def draw(self, screen):

        for i in range(8):
            for j in range(8):
                if self.board[i][j]:
                    self.board[i][j].draw(screen)
