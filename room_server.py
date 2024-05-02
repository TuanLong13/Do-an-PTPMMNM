import socket
import threading
import time

host = '127.0.0.1'

port = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(2)

clients = []
nicknames = []
players = []
sendname = True

def broadcast(message):
    for client in clients:
        client.send(message)

def gamebroadcast(message):
    while len(clients) != 0:
        continue
    for player in players:
        player.send(message)

def handle(client):
    while True:
        message = client.recv(1024).decode()
        print(message)
        if( message != "{quit}" ):
            if( str(message).startswith("GAME") ):
                print(message)
                gamebroadcast(message.encode('utf-8'))
            elif( str(message).startswith("{P1}")):
                print("Player 1 left the game")
                index = players.index(client)
                nickname = nicknames[index]
                players.remove(client)
                nicknames.remove(nickname)
            elif( str(message).startswith("{P2}")):
                print("Player 2 left the game")
                index = players.index(client)
                nickname = nicknames[index]
                players.remove(client)
                nicknames.remove(nickname)
            else:
                index = clients.index(client)
                nickname = nicknames[index]
                messages = f'{nickname}: ' + message
                broadcast(messages.encode('utf-8'))
        else:
            # Xử lý khi client muốn rời khỏi phòng chat
            if( len(clients) == 2 or len(players) == 1 ):
                broadcast(f"PLAYERNAME,{nicknames[0]},{nicknames[1]}".encode('utf-8'))
                try:
                    index = clients.index(client)
                    nickname = nicknames[index]
                    clients.remove(client)
                    players.append(client)
                    broadcast(f'{nickname} đã vào chơi!'.encode('utf-8'))
                except:
                    index = players.index(client)
                    players.remove(players)
            else:
                print("Not enough client")
                broadcast("Chưa đủ người chơi để bắt đầu".encode("utf-8"))
            

# Hàm nhận kết nối từ client
def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        print(f'Nickname of client is {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Khởi động server
print('Server is listening...')
thread = threading.Thread(target=receive)
thread.start()

