import sys
import pygame as pg
from client import Network
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

        play_online_button = Button('PLAY ONLINE', (100, 225, 250, 50), lambda: self.game_page(online=True))
        play_online_button.config(
            hover=(25, 25, 25)
        )

        quit_game_button = Button('QUIT', (100, 300, 250, 50), self.quit)
        quit_game_button.config(
            hover=(25, 25, 25)
        )

        while True:

            self.win.blit(bg, (0, 0))

            new_game_button.draw(self.win)
            play_online_button.draw(self.win)
            quit_game_button.draw(self.win)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    new_game_button.collide(event.pos)
                    play_online_button.collide(event.pos)
                    quit_game_button.collide(event.pos)

            mouse = pg.mouse.get_pos()

            new_game_button.mouseover(self.win, mouse)
            play_online_button.mouseover(self.win, mouse)
            quit_game_button.mouseover(self.win, mouse)

            pg.display.update()

    def loading_page(self):
        self.win.fill((0, 0, 0))
        loading = Label('Finding Player...')
        loading.config(color=(255, 255, 255), font_size=40)
        rect = loading.get_rect()
        rect.center = 500, 320
        loading.draw(self.win, rect.x, rect.y)
        pg.display.update()

    def game_page(self, online=False):

        self.loading_page()

        self.win.fill((255, 0, 0))

        bg = pg.image.load('./assets/board.jpg')
        bg = pg.transform.scale(bg, (680, self.win_height))

        computer = Label('Computer')
        computer.config(
            color=(57, 62, 70),
            font_size=54
        )

        user = Label('User')
        user.config(
            color=(240, 240, 240),
            font_size=54
        )


        black_timer = Label('Black')
        black_timer.config(
            color=(57, 62, 70),
            font_size=48
        )

        black_time = Label('15:00')
        black_time.config(
            color=(57, 62, 70),
            font_size=32
        )

        white_timer = Label('White')
        white_timer.config(
            color=(240, 240, 240),
            font_size=48
        )

        white_time = Label('15:00')
        white_time.config(
            color=(240, 240, 240),
            font_size=32
        )

        player = Network()

        board = Board()
        player_turn = 1

        if online:
            player.connect()
            color = player.recv(13)

            player_turn = 1 if color == 'w' else 0

        message1 = Label('')
        message1.config(color=(255, 255, 255), font_size=48)

        message2 = Label('')
        message2.config(color=(255, 255, 255), font_size=32)

        w_time = b_time = 900

        while True:

            if online and not board.game_over:
                board = player.get_board()
                if board.turn == 1:
                    w_time = 900 - board.white_time_elapsed
                else:
                    b_time = 900 - board.black_time_elapsed

            self.win.blit(bg, (0, 0))

            pg.draw.rect(self.win, (1, 1, 1), (690, 0, 310, 680))

            if online:
                black_timer.draw(self.win, 780, 20)
                black_time.change_text(f'{b_time // 60}:{ f"0{b_time % 60}" if b_time % 60 < 10 else b_time % 60}')
                black_time.draw(self.win, 800, 100)
            else:
                computer.draw(self.win, 750, 20)

            pg.draw.rect(self.win, (255, 0, 0), (690, 150, 310, 10))  # Red Line

            board_message1 = message1.get_rect()
            board_message1.center = (680 + 160, 200)
            message1.draw(self.win, board_message1.x, board_message1.y)

            board_message2 = message2.get_rect()
            board_message2.center = (680 + 160, 250)
            message2.draw(self.win, board_message2.x, board_message2.y)

            pg.draw.rect(self.win, (255, 0, 0), (690, 530, 310, 10))  # Red Line

            if online:
                white_timer.draw(self.win, 780, 550)
                white_time.change_text(f'{w_time // 60}:{ f"0{w_time % 60}" if w_time % 60 < 10 else w_time % 60}')
                white_time.draw(self.win, 800, 630)
            else:
                user.draw(self.win, 790, 550)

            if not online and not board.turn:
                self.call_ai(board)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        if online:
                            player.disconnect()
                        self.menu_page()

                if event.type == pg.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if board.turn == player_turn and not board.game_over:
                        board.select(mx // 85, my // 85)

                        if online:
                            player.send_board(board)

            self.draw(board)

            for i in range(len(board.history)):
                turn, source, dest = board.history[i]
                source = self.get_square(*source)
                dest = self.get_square(*dest)

                history = Label(f'{source}-{dest}')
                history.config(color=(240, 240, 240) if turn == 1 else (57, 62, 70), font_size=24)
                history.draw(self.win, 810, 280 + (i * 40))

            if w_time == 0 or b_time == 0:
                board.game_over = True
                message1.change_text("Time's Up")
                message2.change_text(f'{"Black" if board.turn == 1 else "White"} Wins')
                if online:
                    player.disconnect()
            elif board.game_over and board.check_mate:
                message1.change_text('Check Mate')
                message2.change_text(f'{"Black" if board.turn == 1 else "White"} Wins')
                if online:
                    player.disconnect()
            elif board.game_over:
                message2.change_text('Other Player Left')
                if online:
                    player.disconnect()
            elif board.check:
                message1.change_text('Check')
            else:
                message1.change_text('')
                message2.change_text('')

            pg.display.update()

    def draw(self, board):
        for i in range(8):
            for j in range(8):
                if board.board[i][j]:
                    x = board.board[i][j].px * 85
                    y = board.board[i][j].py * 85

                    # Highlight the block if selected
                    if board.board[i][j].selected:
                        pg.draw.rect(self.win, (255, 214, 107), (x, y, 85, 85))

                    img = pg.image.load(f'./assets/pieces/{board.board[i][j]}.png')
                    img = pg.transform.scale(img, (85, 85))

                    self.win.blit(img, (x, y))

    @staticmethod
    def get_square(my, mx):
        return f'{chr(97 + mx)}{my + 1}'

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
