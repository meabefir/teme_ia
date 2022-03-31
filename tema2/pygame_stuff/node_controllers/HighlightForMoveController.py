import pygame

from .DefaultController import DefaultController
import pygame_stuff.node_controllers.SelectedController as SController
from .MovingController import MovingController

class HighlightForMoveComponent:
    def __init__(self, node, *args):
        self.node = node
        self.tmp_surface = pygame.Surface((self.node.RADIUS*2, self.node.RADIUS*2))
        self.tmp_surface.fill(pygame.Color('white'))

        self.hovered = False

    def init(self):
        pass

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
        # if we got here this cell is empty, we need to move the selected cell to this place
        for _, node in self.node.graph.nodes.items():
            if isinstance(node.controller, SController.SelectedController):
                node.set_controller(MovingController, self.node)
                continue
            node.set_controller(DefaultController)

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