from .Piece import Piece


class Pawn(Piece):
    def __init__(self, color, py, px):
        super().__init__('P', color, py, px)

        self.direction = -1 if color == 'w' else 1  # White pawn moves up and black ones down

    def get_moves(self, board):
        """
        Returns all the possible moves of pawn
        :param board: 8 x 8 board
        :return: set of possible moves
        """
        all_possible_moves = set()

        one_step = True if (0 < self.py < 7 and not board[self.py + self.direction][self.px]) else False
        two_step = False

        if ((self.color == 'b' and self.py == 1)
           or (self.color == 'w' and self.py == 6)) \
           and not board[self.py + self.direction * 2][self.px]:

            two_step = True

        if one_step:
            all_possible_moves.add((self.py + self.direction, self.px))
            if two_step:
                all_possible_moves.add((self.py + self.direction * 2, self.px))

        if 0 < self.py < 7:
            left_attack = board[self.py + self.direction][self.px - 1] if self.px > 0 else None
            right_attack = board[self.py + self.direction][self.px + 1] if self.px < 7 else None

            if right_attack and right_attack.color != self.color:
                all_possible_moves.add((self.py + self.direction, self.px + 1))
            if left_attack and left_attack.color != self.color:
                all_possible_moves.add((self.py + self.direction, self.px - 1))

        return all_possible_moves
