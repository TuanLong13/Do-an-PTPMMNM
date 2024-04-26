import pygame as pg
from Game import *


game = Game("client1")
while True:
    if not game.started:
        game.startScreen()
    else:
        game.playScreen()
        
    pg.display.flip()
