import pygame
import os, sys
import pprint
import random
import copy

from .Node import Node
from .EventManager import EventManager

class Graph:
    def __init__(self, game, nodes=None):
        self.game = game

        self.nodes = nodes if nodes is not None else {}

        if self.nodes == {}:
            self.setup()

    def setup(self):
       self.init_nodes()

    def init_nodes(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

        fin = open(os.path.join(__location__, 'nodes_setup'), 'r')
        s = fin.read()
        s = s.split('\n')
        data = []
        for row in s:
            node, neighs = [s.strip() for s in row.split('-')]
            node = [int(c) for c in node.split()]
            neighs = [[int(c) for c in s.strip().split()] for s in neighs.split(',')]

            data += [[node, neighs]]
        fin.close()

        for node, _ in data:
            x, y = self.game.padding + node[0] * self.game.cell_size, self.game.padding + node[1] * self.game.cell_size
            # setez o culaore random la unele de la inceput
            colors = ["white", "black"]
            color = None
            if random.random() < .4:
                color = random.choice(colors)
            self.nodes[(node[0], node[1])] = Node(self.game, self, (node[0], node[1]), (x, y), value=color)
        for node, neighs in data:
            this_neigh_nodes = []
            for neigh in neighs:
                this_neigh_nodes += [self.nodes[(neigh[0], neigh[1])]]
            self.nodes[(node[0], node[1])].set_neighs(this_neigh_nodes)

            # tmp stc
    def swap_nodes(self, coords_1, coords_2):
        node_1 = self.nodes[coords_1]
        node_2 = self.nodes[coords_2]

        node_1_value = node_1.value
        node_2_value = node_2.value

        node_1.value = node_2_value
        node_2.value = node_1_value

        # stc
        EventManager.emit_signal("next_turn")

    def handle_event(self, event):
        for _, node in self.nodes.items():
            node.handle_event(event)

    def update(self):
        for _, node in self.nodes.items():
            node.update()

    def render(self, screen):
        for board_coords, node in self.nodes.items():
            node.render(screen)