import os
import pygame
from .ColorPicker import ColorPicker
from .Board import Board

# s - serialize -> construieste un string echivalent cu placa de joc
# p - arata informatii despre piese
# a - moc animations - pt testare
# key arrows + hover piece, muta piesa
# f - algoritm de gasire solutie pe placa curenta

class Game:

    def __init__(self, rows=10, cols=10, pos=(100, 100), size=(300, 250), file=""):
        self.board = Board((pos[0], pos[1]), rows, cols, width=200) if file == "" else self.loadFromFile(file)

        self.colorPicker = ColorPicker((pos[0] + size[0] - 100, pos[1]), width=100,
                                       colorChangeCallback=self.board.setSelectedColor)

        self.rows = rows
        self.cols = cols
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])

    def loadFromFile(self, path):
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, path)
        file = open(path, 'r')
        s = file.read().split('\n')

        file.close()
        board = Board((100, 100), len(s), len(s[0]))
        board.loadFromString(s)
        return board

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
