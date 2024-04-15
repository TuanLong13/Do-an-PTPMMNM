from collections import deque
import pygame as pg
from const import *
from Hexagon import *   

import socket
import threading

connection_established = False
class Server_Board:
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

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn, self.addr = (0, 0)

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
                        if self.PLAYER == 1 :
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
                            send_data = '{},{},{},{}'.format(col, row, True, self.PLAYER).encode()
                            self.conn.send(send_data)
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
    def create_thread(self,target):
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
    def waiting_connection(self):
        HOST = "127.0.0.1"
        PORT = 65432
        while True:
            try:
                self.sock.bind((HOST, PORT))
                self.sock.listen(1)
                print("AAAAA")
                self.conn, self.addr = self.sock.accept()
                self.create_thread(self.receive_data)
                return True
            except Exception as e:
                pass

    def receive_data(self):
        while True:
            data = self.conn.recv(1024).decode()
            data = data.split(",")
            x, y = (data[0], data[1])
            if(bool(data[2]) == True):
                self.turn = True
                self.otherCapture(x, y, data[3])
            print(data)
    
    def otherCapture(self, x, y, player):
        self.coordinate[int(x)][int(y)].captured(int(player))