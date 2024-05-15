import socket
import threading
import time

host = '192.168.2.14'
port = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(2)

clients = []
nicknames = []
players = []

def broadcast(message):
    for client in clients:
        client.send(message)

def gamebroadcast(message):
    while len(clients) != 0:
        continue
    for player in players:
        player.send(message)

def handle(client):
    global nicknames
    while True:
        message = client.recv(1024).decode()
        if( message != "{quit}" ):
            if( str(message).startswith("GAME") ):
                gamebroadcast(message.encode('utf-8'))
            elif( str(message).startswith("{P1}")):
                print("Player 1 left the game")
                break
            elif( str(message).startswith("{P2}")):
                print("Player 2 left the game")
                break
            else:
                index = clients.index(client)
                nickname = nicknames[index]
                messages = f'{nickname}: ' + message
                broadcast(messages.encode('utf-8'))

        else:
            # Xử lý khi client muốn rời khỏi phòng
            try:
                index = clients.index(client)
                nickname = nicknames[index]
                clients.remove(client)
                players.append(client)
                broadcast(f'{nickname} đã vào chơi!'.encode('utf-8'))
            except ValueError as e:
                index = players.index(client)
                nickname = nicknames[index]
                players.remove(client)
                broadcast(f'{nickname} đã thoát!'.encode('utf-8'))
                time.sleep(0.01)
                broadcast("{quit}".encode("utf-8"))
                if( len(players) == 1 ):
                    (players.pop()).send("{back}".encode("utf-8"))
                    nicknames = []
                break

            

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
        if( len(clients) == 2 ):
            time.sleep(0.01)
            broadcast(f"PLAYERNAME,{nicknames[0]},{nicknames[1]}".encode('utf-8'))
            time.sleep(0.01)
            broadcast("{start}".encode("utf-8"))

# Khởi động server
print('Server is listening...')
thread = threading.Thread(target=receive)
thread.start()

