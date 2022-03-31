import pygame

from .HighlightForMoveController import HighlightForMoveComponent
from .DefaultController import DefaultController

class SelectedController:
    def __init__(self, node, *args):
        self.node = node

    def init(self):
        for _, node in self.node.graph.nodes.items():
            if node == self.node:
                continue
            if node.is_neigh_with(self.node) and node.value is None:
                node.set_controller(HighlightForMoveComponent, self.node.board_coords)
                continue
            node.set_controller(DefaultController)

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def render(self, screen):
        pygame.draw.circle(screen, pygame.Color("red"), self.node.coords, self.node.RADIUS+6)

        if self.node.value == 'black':
            pygame.draw.circle(screen, pygame.Color('black'), self.node.coords, self.node.RADIUS)
        else:
            pygame.draw.circle(screen, pygame.Color('black'), self.node.coords,
                               self.node.RADIUS)
            pygame.draw.circle(screen, pygame.Color('white'), self.node.coords,
                               self.node.RADIUS-3)