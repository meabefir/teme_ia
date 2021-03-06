import pygame

from .SelectedController import SelectedController
from ..Helper import *
from .DefaultController import DefaultController
from ..EventManager import EventManager

class HighlightController:
    def __init__(self, node, *args):
        self.node = node
        self.tmp_surface = pygame.Surface((self.node.RADIUS*2, self.node.RADIUS*2))
        self.tmp_surface.fill(pygame.Color('white'))

        self.hovered = False

    def init(self):
        # print(self.node.value is not None and self.node.game.min_color != self.node.value)
        if self.node.value is None and self.node.game.min_pieces == 0:
            self.node.set_controller(DefaultController)
            return
        if self.node.value is not None and self.node.game.min_color != self.node.value:
            self.node.set_controller(DefaultController)
            return
        if not self.node.can_be_selected():
            self.node.set_controller(DefaultController)
            return

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.node.mouse_over():
                self.hovered = True
            else:
                self.hovered = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.node.mouse_over():
                self.select()

    def select(self):
        if self.node.value is None:
            self.node.value = self.node.game.min_color
            self.node.game.min_pieces -= 1
            if self.node.graph.formed_line(self.node):
                self.node.graph.capture_mode()
            else:
                # place a piece here
                print(self.node.game.min_pieces)
                EventManager.emit_signal("next_turn")
        else:
            self.node.set_controller(SelectedController)

    def update(self):
        pass

    def render(self, screen):
        if self.hovered:
            self.tmp_surface.set_alpha(150)
        else:
            self.tmp_surface.set_alpha(100)

        if self.node.value is None:
            pygame.draw.circle(self.tmp_surface, pygame.Color('green'), (self.node.RADIUS, self.node.RADIUS), self.node.RADIUS)
        elif self.node.value == 'black':
            pygame.draw.circle(self.tmp_surface, pygame.Color('black'), (self.node.RADIUS, self.node.RADIUS), self.node.RADIUS)
        else:
            pygame.draw.circle(self.tmp_surface, pygame.Color('black'), (self.node.RADIUS, self.node.RADIUS),
                               self.node.RADIUS)
            pygame.draw.circle(self.tmp_surface, pygame.Color('white'), (self.node.RADIUS, self.node.RADIUS),
                               self.node.RADIUS-3)

        screen.blit(self.tmp_surface, (self.node.coords[0] - self.node.RADIUS, self.node.coords[1] - self.node.RADIUS))