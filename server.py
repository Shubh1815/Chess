import socket
import pickle
from collections import deque
from threading import Thread, Lock
from Chess.board import Board

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host, port = 'localhost', 5000

server.bind((host, port))
server.listen()

clients = 0
queue = deque()
games = {}

lock = Lock()


def handle_clients(player_conn, opponent_conn, white_cid, black_cid, color):
    if color == 'w':
        print(f'[ STATUS ] Starting match between {white_cid} & {black_cid}')

    lock.acquire()
    game_board = games[(white_cid, black_cid)]
    lock.release()

    player_conn.send(color.encode())
    player_conn.send(pickle.dumps(game_board))

    while not game_board.game_over:
        p_game_board = player_conn.recv(4096)

        if p_game_board:
            game_board = pickle.loads(p_game_board)
            lock.acquire()
            games[(white_cid, black_cid)] = game_board
            lock.release()
        else:
            lock.acquire()
            games[(white_cid, black_cid)].game_over = True
            lock.release()
            game_board = games[(white_cid, black_cid)]

        try:
            opponent_conn.send(pickle.dumps(game_board))
        except socket.error:
            pass

    player_conn.close()

    game_board = games[(white_cid, black_cid)]
    print(f'[ STATUS ] In {white_cid} vs {black_cid}, {"Black" if game_board.turn == 1 else "White"}')

    lock.acquire()
    if (white_cid, black_cid) in games:
        if game_board.check_mate or (not game_board.check_mate and ['w', 'b'][game_board.turn] == color):
            del games[(white_cid, black_cid)]
    lock.release()


def start_server():
    global clients, queue

    while True:
        conn, addr = server.accept()
        clients += 1
        queue.append((conn, clients))

        print(f'[ NEW CONNECTION ] Total Connection till now: { clients }')

        if len(queue) >= 2:
            white_conn, white_cid = queue.popleft()
            black_conn, black_cid = queue.popleft()

            games[(white_cid, black_cid)] = Board()

            Thread(target=handle_clients, args=(white_conn, black_conn, white_cid, black_cid, 'w')).start()
            Thread(target=handle_clients, args=(black_conn, white_conn, white_cid, black_cid, 'b')).start()


if __name__ == '__main__':
    print('[ STATUS ] Starting Server')
    start_server()
