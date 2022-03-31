import pygame

class DefaultController:
    def __init__(self, node, *args):
        self.node = node

    def init(self):
        pass

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def render(self, screen):
        if self.node.value is None:
            return
        elif self.node.value == 'black':
            pygame.draw.circle(screen, pygame.Color('black'), self.node.coords, self.node.RADIUS)
        else:
            pygame.draw.circle(screen, pygame.Color('black'), self.node.coords,
                               self.node.RADIUS)
            pygame.draw.circle(screen, pygame.Color('white'), self.node.coords,
                               self.node.RADIUS-3)