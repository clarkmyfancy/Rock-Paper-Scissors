from socket import socket, AF_INET, SOCK_STREAM
import pickle

# responsible for connecting to server
class Network:
    def __init__(self):
        self.client = socket(AF_INET, SOCK_STREAM)
        # this server address needs to match the ip address of the machine
        #   running the server. That also needs to be updated in the Server.py file
        self.server = "10.0.18.251"
        self.port = 5555
        self.address = (self.server, self.port)
        self.player = self.connect()

    def connect(self):
        try:
            self.client.connect(self.address)
            return pickle.loads(self.client.recv(2048))
        except:
            print("Connection not successful")

    def get_player(self):
        return self.player

    def send(self, player):
        try:
            self.client.send(pickle.dumps(player))
            player = pickle.loads(self.client.recv(2048))
            return player
        except socket.error as e:
            print(str(e))