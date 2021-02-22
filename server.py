import socket
import pickle
from collections import deque
from threading import Thread, Lock
from Chess.board import Board
import datetime as dt

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host, port = '', 5555

server.bind((host, port))
server.listen()

clients = 0
queue = deque()
games = {}

lock = Lock()


def recv_board(conn, payload_size):
    board = []

    while payload_size > 0:
        buffer_size = min(48, payload_size)
        packet = conn.recv(buffer_size)
        payload_size -= buffer_size

        board.append(packet)

    return b"".join(board)


def handle_clients(player_conn, white_cid, black_cid, color):
    if color == 'w':
        print(f'[ STATUS ] Starting match between {white_cid} & {black_cid}')

    lock.acquire()
    game_board = games[(white_cid, black_cid)]['board']
    lock.release()

    player_conn.send(color.encode('utf-16'))

    player_start_time = dt.datetime.now()
    elapsed_time = 0
    curr_elapsed_time = 0
    colors = ['b', 'w']

    while not game_board.game_over:
        header = player_conn.recv(48)

        if header:
            header = header.decode('utf-16')
            action, payload_size = header.split('\n')
            action = action.split(':')[1]
            payload_size = int(payload_size.split(':')[1])

            if action == 'GET':
                player_conn.send(pickle.dumps(games[(white_cid, black_cid)]['board']))

            if action == 'PUT':
                game_board = pickle.loads(recv_board(player_conn, payload_size))
                lock.acquire()
                games[(white_cid, black_cid)]['board'] = game_board
                lock.release()
        else:
            lock.acquire()
            games[(white_cid, black_cid)]['board'].game_over = True
            lock.release()

        if colors[game_board.turn] == color:
            curr_elapsed_time = round((dt.datetime.now() - player_start_time).total_seconds())

            lock.acquire()
            if color == 'w':
                games[(white_cid, black_cid)]['board'].white_time_elapsed = elapsed_time + curr_elapsed_time
            else:
                games[(white_cid, black_cid)]['board'].black_time_elapsed = elapsed_time + curr_elapsed_time
            lock.release()
        else:
            player_start_time = dt.datetime.now()
            elapsed_time += curr_elapsed_time
            curr_elapsed_time = 0

        game_board = games[(white_cid, black_cid)]['board']

    if not games[(white_cid, black_cid)]['winner']:
        lock.acquire()
        if not games[(white_cid, black_cid)]['board'].check_mate:
            if color == 'w':
                games[(white_cid, black_cid)]['winner'] = 'Black'
            else:
                games[(white_cid, black_cid)]['winner'] = 'White'
        else:
            if color == 'w':
                games[(white_cid, black_cid)]['winner'] = 'White'
            else:
                games[(white_cid, black_cid)]['winner'] = 'Black'
        lock.release()
    else:
        print(f"[ STATUS ] In {white_cid} vs {black_cid}, {games[(white_cid, black_cid)]['winner']} wins")
        del games[(white_cid, black_cid)]

    player_conn.close()


def start_server():
    global clients, queue
    print('[ STATUS ] Starting Server')

    while True:
        conn, addr = server.accept()
        clients += 1
        queue.append((conn, clients))

        print(f'[ NEW CONNECTION ] Total Connection till now: { clients }')

        if len(queue) >= 2:
            white_conn, white_cid = queue.popleft()
            black_conn, black_cid = queue.popleft()

            games[(white_cid, black_cid)] = {
                'board': Board(),
                'winner': None
            }

            Thread(target=handle_clients, args=(white_conn, white_cid, black_cid, 'w')).start()
            Thread(target=handle_clients, args=(black_conn, white_cid, black_cid, 'b')).start()


if __name__ == '__main__':
    start_server()
