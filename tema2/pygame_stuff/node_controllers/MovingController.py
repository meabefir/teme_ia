import pygame

from ..Helper import *
from .DefaultController import DefaultController

class MovingController:
    def __init__(self, node, target_node, *args):
        self.target_node = target_node
        self.original_coords = node.coords
        self.node = node
        self.secs = 1
        self.vel = ((self.target_node.coords[0] - self.node.coords[0]) / 60, (self.target_node.coords[1] - self.node.coords[1]) / 60)

    def init(self):
        pass

    def handle_event(self, event):
        pass

    def update(self):
        self.node.coords = (self.node.coords[0] + self.vel[0], self.node.coords[1] + self.vel[1])

        if squared_distance(self.node.coords, self.target_node.coords) < squared_distance((0,0), self.vel):
            # reset stuff over here
            # reset its position back and switch the node values
            # idle all nodes
            for _, node in self.node.graph.nodes.items():
                node.set_controller(DefaultController)
            self.node.coords = self.original_coords
            # operation graph to swap those two
            self.node.graph.swap_nodes(self.node.board_coords, self.target_node.board_coords)

    def render(self, screen):
        if self.node.value == 'black':
            pygame.draw.circle(screen, pygame.Color('black'), self.node.coords, self.node.RADIUS)
        else:
            pygame.draw.circle(screen, pygame.Color('black'), self.node.coords,
                               self.node.RADIUS)
            pygame.draw.circle(screen, pygame.Color('white'), self.node.coords,
                               self.node.RADIUS - 3)