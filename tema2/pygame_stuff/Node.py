import pygame
from .EventManager import EventManager
from .Helper import *
from enum import Enum
import random
from .node_controllers.DefaultController import *
from .node_controllers.HighlightController import *

class NodeState(Enum):
    NEUTRAL = 1
    HIGHLIGHTED = 2
    HIGHLIGHT_HOVERED = 3
    MOVE_HIGHLIGHTED = 4
    MOVE_HIGHLIGHT_HOVERED = 5
    SELECTED = 6

class Node:
    RADIUS = 20

    def __init__(self, game, graph, board_coords, coords, value=None):
        self.game = game
        self.graph = graph
        self.board_coords = board_coords
        self.coords = coords
        self.neighs = []
        self.font = pygame.font.Font('freesansbold.ttf', 10)

        self.value = value
        self.controller = None
        self.set_controller(DefaultController)

        EventManager.connect("min_turn", self.min_turn)
        EventManager.connect("max_turn", self.max_turn)

    def is_neigh_with(self, node):
       return node in self.neighs

    def min_turn(self, *args):
        self.set_controller(HighlightController)

    def max_turn(self, *args):
        self.set_controller(DefaultController)

    def set_controller(self, class_name, *args):
        self.controller = class_name(self, *args)
        self.controller.init()

    def mouse_over(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if squared_distance((mouse_x, mouse_y), self.coords) > pow(self.RADIUS, 2):
            return False
        else:
            return True

    def set_neighs(self, neighs):
        self.neighs = neighs

    def handle_event(self, event):
        self.controller.handle_event(event)
        pass

    def can_be_selected(self):
        if self.value is None:
            return True
        else:
            return self.can_move()

    def can_move(self):
        for neigh in self.neighs:
            if neigh.value is None:
                return True
        return False

    def update(self):
        self.controller.update()

        pass

    def render_node_controller(self, screen):
        text = self.font.render(self.controller.__class__.__name__, True, pygame.Color("black"))
        text_rect = text.get_rect()
        text_rect.center = (self.coords[0], self.coords[1] - 20)

        screen.blit(text, text_rect)

    def render_debug(self, screen):
        self.render_node_controller(screen)

    def render(self, screen):
        self.controller.render(screen)

        self.render_debug(screen)

        # debug
        # draw text here boardcoords

        # just a test
        # for neigh in self.neighs:
        #     pygame.draw.line(screen, pygame.Color("green"), self.coords, neigh.coords)

    def __str__(self):
        ret = ""
        ret += f'{self.board_coords} - {self.value}'
        return ret