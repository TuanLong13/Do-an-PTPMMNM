import pygame as pg
from pygame import gfxdraw
from const import *
class PlayerTag:
    def __init__(self, surface, txt, pos, size, color):
        self.surface = surface
        self.text = txt
        self.pos = pos
        self.size = size
        self.color = color
        self.originalColor = color
        self.rect = pg.Rect(20, 40, 20, 20)
    
    def render(self):
        """Vẽ nút bấm ra màn hình"""
        self.color = self.originalColor
        self.printText(self.size)
    
    def renderFlip(self):
        """Vẽ nút bấm xoay ngược ra màn hình"""
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.color = ORANGE
            self.printFlipText(self.size-10)
        else:
            self.color = self.originalColor
            self.printFlipText(self.size)
        
    def printText(self, size):
        """In text ra màn hình"""
        font = pg.font.SysFont('Verdana', size)
        text = font.render(str(self.text), False, WHITE, self.color)
        self.rect = text.get_rect(bottomleft = self.pos)
        self.surface.blit(text, self.rect)     

    def printFlipText(self, size):
        """In text xoay ngược ra màn hình"""
        font = pg.font.SysFont('Verdana', size)
        text = font.render(self.text, False, self.color)
        text = pg.transform.flip(text, False, True)
        self.rect = text.get_rect(center = self.pos)
        self.surface.blit(text, self.rect)     