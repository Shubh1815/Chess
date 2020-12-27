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

        black_timer = Label('Black')
        black_timer.config(
            color=(255, 255, 255),
            font_size=48
        )

        black_time = Label('15:00')
        black_time.config(
            color=(255, 255, 255),
            font_size=32
        )

        white_timer = Label('White')
        white_timer.config(
            color=(255, 255, 255),
            font_size=48
        )

        white_time = Label('15:00')
        white_time.config(
            color=(255, 255, 255),
            font_size=32
        )

        board = Board()

        while True:

            self.win.blit(bg, (0, 0))
            pg.draw.rect(self.win, (1, 1, 1), (690, 0, 310, 680))

            black_timer.draw(self.win, 780, 20)
            black_time.draw(self.win, 800, 100)

            pg.draw.rect(self.win, (255, 0, 0), (690, 150, 310, 10))  # Red Line

            board_message1 = board.message1.get_rect()
            board_message1.center = (680 + 160, 200)
            board.message1.draw(self.win, board_message1.x, board_message1.y)

            board_message2 = board.message2.get_rect()
            board_message2.center = (680 + 160, 250)
            board.message2.draw(self.win, board_message2.x, board_message2.y)

            pg.draw.rect(self.win, (255, 0, 0), (690, 530, 310, 10))  # Red Line

            white_timer.draw(self.win, 780, 550)
            white_time.draw(self.win, 800, 630)

            if not board.turn:
                self.call_ai(board)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    mx, my = event.pos

                    if board.turn:
                        board.select(mx // 85, my // 85)

            board.draw(self.win)

            if board.game_over:
                board.message1.change_text('Check Mate')
                board.message2.change_text(f'{"Black" if board.turn == 1 else "White"} Wins')
            elif board.check:
                board.message1.change_text('Check')

            pg.display.update()

    @staticmethod
    def call_ai(board):
        if not board.game_over and not board.turn:
            get_best_move(board, board.turn)

    @staticmethod
    def quit():
        pg.quit()
        sys.exit()


if __name__ == '__main__':

    app = Game()
    app.menu_page()
