import pygame
from .ColorPicker import ColorPicker

class Cell:

    def __init__(self, value, row, col, pos, size):
        self.row = row
        self.col = col
        self.value = value
        self.rect = pygame.Rect(pos[0], pos[1], size, size)
        self.pos = [pos[0], pos[1]]

    def move(self, dx, dy):
        # self.rect.move_ip(dx, dy)
        self.pos[0] += dx
        self.pos[1] += dy
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def assignValue(self, value):
        self.value = value

    def isMouseOver(self):
        x, y = pygame.mouse.get_pos()
        return self.rect.collidepoint(x, y)

    def render(self, screen):
        if self.value == '#':
            pygame.draw.rect(screen, pygame.Color("brown"), self.rect)
            return
        elif self.value == '.':
            return
        else:
            pygame.draw.rect(screen, ColorPicker.COLORS[self.value], self.rect)