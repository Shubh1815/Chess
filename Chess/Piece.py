class Piece:

    def __init__(self, name, color, py, px):
        self.name = name
        self.color = color
        self.px = px
        self.py = py

        self.selected = 0

    def move_row(self, board):
        """
        Returns possible moves in a row for a piece
        :param board: 8 x 8 Array
        :return: set of moves possible
        """
        all_possible_move = set()

        i = self.py
        l = r = self.px

        while l > 0:
            l -= 1
            if board[i][l]:
                if board[i][l].color != self.color:
                    all_possible_move.add((i, l))
                break

            all_possible_move.add((i, l))

        while r < 7:
            r += 1
            if board[i][r]:
                if board[i][r].color != self.color:
                    all_possible_move.add((i, r))
                break

            all_possible_move.add((i, r))

        return all_possible_move

    def move_col(self, board):
        """
        Returns possible moves in a col for a piece
        :param board: 8 x 8 Array
        :return: set of moves possible
        """
        all_possible_move = set()

        u = d = self.py
        j = self.px

        while u > 0:
            u -= 1
            if board[u][j]:
                if board[u][j].color != self.color:
                    all_possible_move.add((u, j))
                break

            all_possible_move.add((u, j))

        while d < 7:
            d += 1
            if board[d][j]:
                if board[d][j].color != self.color:
                    all_possible_move.add((d, j))
                break

            all_possible_move.add((d, j))

        return all_possible_move

    def move_diagonal(self, board):
        """
        Returns possible moves in diagonals for a piece
        :param board: 8 x 8 Array
        :return: set of moves possible
        """

        all_possible_move = set()

        i, j = self.py, self.px

        # Upper Left
        while i > 0 and j > 0:
            i -= 1
            j -= 1
            if board[i][j]:
                if board[i][j].color != self.color:
                    all_possible_move.add((i, j))
                break

            all_possible_move.add((i, j))

        i, j = self.py, self.px

        # Upper Right
        while i > 0 and j < 7:
            i -= 1
            j += 1
            if board[i][j]:
                if board[i][j].color != self.color:
                    all_possible_move.add((i, j))
                break

            all_possible_move.add((i, j))

        i, j = self.py, self.px

        # Bottom Left
        while i < 7 and j > 0:
            i += 1
            j -= 1

            if board[i][j]:
                if board[i][j].color != self.color:
                    all_possible_move.add((i, j))
                break

            all_possible_move.add((i, j))

        i, j = self.py, self.px

        # Bottom Right
        while i < 7 and j < 7:
            i += 1
            j += 1
            if board[i][j]:
                if board[i][j].color != self.color:
                    all_possible_move.add((i, j))
                break

            all_possible_move.add((i, j))

        return all_possible_move

    def select(self):
        self.selected ^= 1

    def move_position(self, mx, my):
        self.px = mx
        self.py = my

    def __str__(self):
        return f"{self.color}{self.name}"
