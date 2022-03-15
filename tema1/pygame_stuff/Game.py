import pygame
from .ColorPicker import ColorPicker
from .Board import Board

class Game:

    def __init__(self, rows=10, cols=7, pos=(100, 100), size=(300,250)):
        self.board = Board((pos[0], pos[1]), rows, cols, width=200)
        self.colorPicker = ColorPicker((pos[0] + size[0] - 100, pos[1]), width=100, colorChangeCallback=self.board.setSelectedColor)

        self.rows = rows
        self.cols = cols
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])

    def handleEvent(self, event):
        rez = self.colorPicker.handleEvent(event)
        if rez:
            return
        rez = self.board.handleEvent(event)
        if rez:
            return
        # handle yours

    def update(self):
        self.board.update()

    def render(self, screen):
        # draw me
        # pygame.draw.rect(screen, pygame.Color("white"), self.rect, 2)

        self.colorPicker.render(screen)
        self.board.render(screen)