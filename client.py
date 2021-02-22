import pickle
import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = 'localhost'
        self.port = 5555
        self.addr = (self.host, self.port)

    def send_board(self, board):
        board = pickle.dumps(board)
        size = str(len(board))
        size = ("0" * max(0, 4 - len(size))) + size

        self.send(f"ACTION:PUT\nPAYLOAD:{size}")
        self.send(board, pickled=True)

    def get_board(self):
        self.send("ACTION:GET\nPAYLOAD:0000")

        board = []
        packet = self.client.recv(4096)
        while True:
            if not packet:
                break
            board.append(packet)
            try:
                pickle.loads(b"".join(board))
                break
            except pickle.UnpicklingError:
                packet = self.client.recv(4096)

        return pickle.loads(b"".join(board))

    def send(self, data, pickled=False):
        if not pickled:
            self.client.send(data.encode('utf-16'))
        else:
            self.client.send(data)

    def recv(self, buffer_size=1024):
        return self.client.recv(buffer_size).decode('utf-16')

    def connect(self):
        self.client.connect(self.addr)

    def disconnect(self):
        self.client.close()
