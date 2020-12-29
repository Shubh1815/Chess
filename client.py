import pickle
import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '54.147.30.202'
        self.port = 5000
        self.addr = (self.host, self.port)

    def send_board(self, board):
        board = pickle.dumps(board)
        self.client.send(board)

    def recv_board(self):
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

    def send(self, data):
        self.client.send(data.encode())

    def recv(self):
        return self.client.recv(1024).decode('utf-8')

    def connect(self):
        self.client.connect(self.addr)

    def disconnect(self):
        self.client.close()
