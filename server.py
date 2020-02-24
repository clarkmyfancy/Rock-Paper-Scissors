
import pickle
from socket import socket, error, AF_INET, SOCK_STREAM
from  _thread import *

from game import Game

server = "10.0.18.251"
port = 5555
max_clients_at_once = 2

socket = socket(AF_INET, SOCK_STREAM)

try: 
    socket.bind((server, port))
except error as e:
    print(str(e))

print("Waiting for connection, server started")
socket.listen(max_clients_at_once)

connected = set()
games = {}
id_count = 0

def client_thread(connection, player, game_id):
    global id_count
    connection.send(str.encode(str(player)))
    reply = ""
    while True:
        try:
            if not game_id in games:
                break
            game = games[game_id]
            data = connection.recv(4096).decode()
            if not data:
                break
            if data == "reset":
                game.reset_did_go()
            elif data != "get":
                game.play(player, data)

            reply = game
            connection.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    try:
        if games[game_id]:
            del games[game_id]
        print("Closing game", game_id)
    except:
        raise Exception("unable to delete game")
    id_count -= 1
    connection.close()

# def handle_move(game, player, data):
#     if data == "reset":
#         game.reset()
#     elif data != "get":
#         game.play(player, data)
#     return game

def extract_meta_info_and_log(address):
    local_ip, port = extract_ip_and_port_as_string(address)
    print("Connected to local ip: " + local_ip + " on port: " + port)

def extract_ip_and_port_as_string(address):
    return address[0], str(address[1])
 
while True:
    connection, address = socket.accept()
    extract_meta_info_and_log(address)

    id_count += 1
    player = 0 
    game_id = (id_count - 1) // 2
    if id_count % 2 == 1:
        games[game_id] = Game(game_id)
        print("Creating a new game.")
    else:
        games[game_id].ready = True
        player = 1
    start_new_thread(client_thread, (connection, player, game_id))

socket.close()