import pickle
import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = 'localhost'
        self.port = 5000
        self.addr = (self.host, self.port)

    def send_board(self, board):
        board = pickle.dumps(board)
        self.client.send(board)

    def recv_board(self):
        board = self.client.recv(4096)
        board = pickle.loads(board)

        return board

    def send(self, data):
        self.client.send(data.encode())

    def recv(self):
        return self.client.recv(1024).decode('utf-8')

    def connect(self):
        self.client.connect(self.addr)

    def disconnect(self):
        self.client.close()
