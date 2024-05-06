from collections import deque
import tkinter
from tkinter import Tk
import pygame as pg
from const import *
from Hexagon import *   
import socket
import threading

class Client1_Board:
    def __init__(self, surface, size):
        self.surface = surface
        self.TILES = size
        self.HEXRADIUS = H/(20 + self.TILES*2)
        #Khởi tạo toạ độ board
        self.coordinate = [[0 for i in range(self.TILES)] for j in range(self.TILES)]
        #Danh sách các ô trong board
        self.listHexagon = []
        #Danh sách các ô giáp đường viền đỏ
        self.redBorder = []
        #Danh sách các ô giáp đường viền xanh
        self.blueBorder = []
        self.PLAYER = 1
        self.turn = True
        self.player1 = "player1"
        self.player2 = "player2"
        self.interupt = False # Biến gián đoạn cuộc chơi 

    
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def drawRect(self, surface, pos, height, boardSize):
        """Vẽ đường viền cho board"""
        x, y = pos
        pg.draw.polygon(surface, RED, [(x,y), (x, y+height), (x+height-height/boardSize, y+height/2), (x+height-height/boardSize ,y+height/2+height)])
        pg.draw.polygon(surface, BLUE, [(x,y), (x+height-height/boardSize, y+height/2), (x, y+height), (x+height-height/boardSize, y+height/2+height)])

    def createBoard(self):   
        """Tạo board"""
        x, y = STARTPOS
        for i in range(self.TILES):
            distance = 0
            for j in range(self.TILES):
                self.coordinate[i][j] = Hexagon(self.HEXRADIUS, (x, y+distance))
                distance += self.coordinate[i][j].minimalRadius * 2
                self.listHexagon.append(self.coordinate[i][j])
                if i == self.TILES-1:
                    self.redBorder.append(self.coordinate[i][j])
                if j == self.TILES-1:
                    self.blueBorder.append(self.coordinate[i][j])
            x, y = self.coordinate[i][0].findNextPoint()

    def resetBoard(self):
        """Reset trạng thái board"""
        for hexagon in self.listHexagon:
            hexagon.state = 0
        self.sock.send(bytes("{P1}", "utf8"))
        self.sock.close()

    def showBoard(self):
        """Vẽ board ra màn hình"""
        x, y = STARTPOS
        self.drawRect(self.surface,(x-2*self.coordinate[0][0].minimalRadius, y - 4 * self.coordinate[0][0].minimalRadius), self.coordinate[0][0].minimalRadius * (self.TILES+2) * 2, self.TILES)
        for col in range(self.TILES):
            for row in range(self.TILES):
                if self.coordinate[col][row].state == 0:
                    self.coordinate[col][row].fillHexagon(self.surface, WHITE)
                    self.coordinate[col][row].render(self.surface)
                    if self.coordinate[col][row].inHexagon(pg.mouse.get_pos()):
                        if self.PLAYER == 1:
                            self.coordinate[col][row].fillHexagon(self.surface, RED)
                            self.coordinate[col][row].render(self.surface)
                elif self.coordinate[col][row].state == 1:
                    self.coordinate[col][row].fillHexagon(self.surface, RED)
                    self.coordinate[col][row].render(self.surface)
                else:
                    self.coordinate[col][row].fillHexagon(self.surface, BLUE)
                    self.coordinate[col][row].render(self.surface)

    def capture(self, sound):
        """Khi người chơi click vào 1 ô trắng thì ô sẽ chuyển màu thành màu của ng chơi đó"""
        for col in range(self.TILES):
            for row in range(self.TILES):
                if self.coordinate[col][row].inHexagon(pg.mouse.get_pos())\
                    and self.coordinate[col][row].state == 0 and self.turn == True:
                        if self.PLAYER == 1:
                            pg.mixer.Sound.play(sound)
                            self.coordinate[col][row].captured(self.PLAYER)
                            send_data = '{},{},{},{},{}'.format('GAME',col, row, True, self.PLAYER).encode()
                            self.sock.send(send_data)
                            self.turn = False
                        
    
    def DFS(self, start, finish, player):
        """Thuật toán tìm theo chiều sâu"""
        stack = deque()
        stack.append(start)
        visited = []
        while len(stack):
            current = stack.pop()
            for hexagon in finish:
                if current is hexagon:
                    return True
            visited.append(current)
            listNeighbour = current.findAllNeighbour(self.listHexagon)
            for hexagon in listNeighbour:
                if hexagon not in visited and hexagon.state == player:
                    stack.append(hexagon)
        return False
    
    def checkWin(self):
        """TÌm người chiến thắng bằng thuật toán DFS"""
        for row in range(self.TILES):
            if self.coordinate[0][row].state == 1:
                if self.DFS(self.coordinate[0][row], self.redBorder, 1):
                    return 1
        for col in range(self.TILES):
            if self.coordinate[col][0].state == 2:
                if self.DFS(self.coordinate[col][0], self.blueBorder, 2):
                    return 2
        return 0
    
    def create_thread(self, target):
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()

    def receive_data(self):
        while True:
            message = self.sock.recv(1024).decode()
            if( str(message).startswith("{back}") ):
                self.interupt = True
                break
            elif( str(message).startswith("{start}") ):
                self.begin_button["state"] = "normal"
            elif( str(message).startswith("{quit}") ):
                self.begin_button["state"] = "disabled"
            elif( str(message).startswith("PLAYERNAME") ):
                data = message.split(",")
                self.player1 = str(data[1])
                self.player2 = str(data[2])
            else:
                if( str(message).startswith("GAME") ):
                    data = message.split(",")
                    x, y = (data[1], data[2])
                    if(bool(data[3]) == True and int(data[4]) == 2):
                        self.turn = True
                        self.otherCapture(x, y, data[4])
                else:
                    try:
                        self.msg_list.insert(tkinter.END, message)
                    except:
                        print('An error occurred!')
                

    def otherCapture(self, x, y, player):
        self.coordinate[int(x)][int(y)].captured(int(player))


                    #                           Chat room

    def waiting_connection(self):
        HOST = '192.168.147.77'
        PORT = 5000
        while True:
            try:
                self.sock.connect((HOST, PORT))
                self.create_thread(self.receive_data)
                self.create_chat_UI()
                return True
            except Exception as e:
                pass

    def create_chat_UI(self):    
        self.top = Tk()
        self.top.title("Phòng chat")

        messages_frame = tkinter.Frame(self.top)
        self.my_msg = tkinter.StringVar()  # For the messages to be sent.
        self.my_msg.set("Nhập nickname của bạn")
        
        scrollbar = tkinter.Scrollbar(messages_frame)  # To see through previous messages.
        # this will contain the messages. 
        self.msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.msg_list.pack()
        messages_frame.pack()

        entry_field = tkinter.Entry(self.top, textvariable=self.my_msg)
        entry_field.bind("<Return>", self.send)
        entry_field.pack()

        send_button = tkinter.Button(self.top, text="Gửi", command=self.send)
        send_button.pack()

        self.begin_button = tkinter.Button(self.top, text="Bắt đầu game", command=self.on_closing)
        self.begin_button.pack()
        self.begin_button["state"] = "disable"

        self.top.protocol("WM_DELETE_WINDOW", self.on_closing)
        tkinter.mainloop()  # for start of GUI  Interface
        
    def send(self, event=None):  # event is passed by binders.play
        msg = self.my_msg.get()
        self.my_msg.set("")  # Clears input field.
        self.sock.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            self.top.destroy()
    def on_closing(self, event=None):
        """This function is to be called when the window is closed."""
        self.my_msg.set("{quit}")
        self.send()
    def quit_game(self):
        self.sock.send("{quit}".encode("utf-8"))
        self.resetBoard()
   