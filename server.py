from player import Player 
import pickle
from socket import socket, error, AF_INET, SOCK_STREAM
from  _thread import *
import sys
import os
import time

# socket allows connections to come into the server on a given port
# the server variable will be an ip address 
server = "10.0.18.251"
port = 5555
max_clients_at_once = 2

# ipv4, type of socket, sockstream is how the server string comes in?
socket = socket(AF_INET, SOCK_STREAM)

try: 
    socket.bind((server, port))
except error as e:
    print(str(e))

print("Waiting for connection, server started")
socket.listen(max_clients_at_once)

players = [
    Player((0, 0), 50, 50, (255, 0, 0)),
    Player((100, 100), 50, 50, (180, 140, 15))
]

def client_thread(connection, _current_player):
    player_index = 0 if _current_player > 0 else 1
    connection.send(pickle.dumps(players[player_index]))
    msg = ""
    connectedToClient = True
    while connectedToClient:
        print()
        # IF YOU GET ANY ERRORS LIKE 'thing was truanced in size' 
        #   or whatever, just increase this number
        player = pickle.loads(connection.recv(2048))
        players[player_index] = player

        if not player:
            print("Player was not received")
            connectedToClient = False
            break 

        if player_index == 0:
            msg = players[1]
        else:
            msg = players[0]

        print("Server received: ", player)
        print("Server responded with: ", msg)
        # encodes string into a bytes object, security thing
        connection.sendall(pickle.dumps(msg))
    print("Lost connection")
    print("________________________________")
    connection.close()

def extract_meta_info_and_log(address):
    local_ip, port = extract_ip_and_port_as_string(address)
    print("Connected to local ip: " + local_ip + " on port: " + port)

def extract_ip_and_port_as_string(address):
    return address[0], str(address[1])

current_player = 1
while True:
    connection, address = socket.accept()
    extract_meta_info_and_log(address)
    start_new_thread(client_thread, (connection, current_player))
    current_player *= -1
socket.close()