import sys
import pygame as pg
from utils import Button, Label
from Chess.board import Board
from Chess.Ai import get_best_move


class Game:
    def __init__(self):
        pg.init()

        self.win_width = 1000
        self.win_height = 680

        self.win = pg.display.set_mode((self.win_width, self.win_height))
        pg.display.set_caption('Chess')

    def menu_page(self):
        bg = pg.image.load('./assets/bg.jpg')
        bg = pg.transform.scale(bg, (self.win_width, self.win_height))

        new_game_button = Button('NEW GAME', (100, 150, 250, 50), self.game_page)
        new_game_button.config(
            hover=(25, 25, 25)
        )

        quit_game_button = Button('QUIT', (100, 225, 250, 50), self.quit)
        quit_game_button.config(
            hover=(25, 25, 25)
        )

        while True:

            self.win.blit(bg, (0, 0))

            new_game_button.draw(self.win)
            quit_game_button.draw(self.win)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    new_game_button.collide(event.pos)
                    quit_game_button.collide(event.pos)

            mouse = pg.mouse.get_pos()

            new_game_button.mouseover(self.win, mouse)
            quit_game_button.mouseover(self.win, mouse)

            pg.display.update()

    def game_page(self):
        self.win.fill((255, 0, 0))

        bg = pg.image.load('./assets/board.jpg')
        bg = pg.transform.scale(bg, (680, self.win_height))

        timer = Label('TIME')
        timer.config(
            color=(255, 255, 255),
            font_size=48
        )

        time = Label('00:00')
        time.config(
            color=(255, 255, 255),
            font_size=32
        )

        board = Board(680, 680)

        while True:

            self.win.blit(bg, (0, 0))
            pg.draw.rect(self.win, (1, 1, 1), (690, 0, 310, 680))
            pg.draw.rect(self.win, (255, 0, 0), (690, 200, 310, 10))

            timer.draw(self.win, 780, 20)
            time.draw(self.win, 800, 100)

            board.draw(self.win)

            board_message = board.message.get_rect()
            board_message.center = (680 + 160, 250)

            board_message_victory = board.message_victory.get_rect()
            board_message_victory.center = (680 + 160, 300)

            board.message.draw(self.win, board_message.x, board_message.y)
            board.message_victory.draw(self.win, board_message_victory.x, board_message_victory.y)

            if not board.turn:
                self.call_ai(board)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    mx, my = event.pos

                    if board.turn:
                        board.clicked(mx, my)
                        pg.display.update()

            pg.display.update()

    @staticmethod
    def quit():
        pg.quit()
        sys.exit()

    @staticmethod
    def call_ai(board):
        if not board.turn and not board.game_over:
            board.selected_piece = None
            i, j = get_best_move(board, board.turn)
            si, sj = board.selected_piece
            print(board.clicked(j, i, ai=True))
            print(board.checked)
            print((si, sj), 'to', (i, j))
            # board.turn = 1


if __name__ == '__main__':

    app = Game()
    app.menu_page()
