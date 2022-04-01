import pygame
import os, sys
import pprint
import random
import copy
from pprint import pprint

from .Node import Node
from .EventManager import EventManager
from .node_controllers.DefaultController import DefaultController
from .node_controllers.CaptureController import CaptureController

class Graph:
    def __init__(self, game, nodes=None):
        self.game = game

        self.nodes = nodes if nodes is not None else {}
        self.lines = self.read_lines()

        if self.nodes == {}:
            self.setup()

    def setup(self):
       self.init_nodes()

    def read_lines(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        fin = open(os.path.join(__location__, 'lines_setup'), 'r')
        s = fin.read()
        s = s.split('\n')
        data = []
        for row in s:
            row = row.split(',')
            data += [[[int(sub) for sub in el.split(' ')] for el in [coord.strip() for coord in row]]]
        fin.close()
        pprint(data)
        return data

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
            # stc tmp to populate board randomly
            if random.random() < .4:
                color = random.choice(colors)
                if color == self.game.min_color:
                    if self.game.min_pieces == 0:
                        color = None
                    else:
                        self.game.min_pieces -= 1
                elif color == self.game.max_color:
                    if self.game.max_pieces == 0:
                        color = None
                    else:
                        self.game.max_pieces -= 1

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

    def formed_line(self, node):
        node_board_coords = node.board_coords
        for line in self.lines:
            if list(node_board_coords) not in line:
                continue
            node_1, node_2, node_3 = self.nodes[tuple(line[0])], self.nodes[tuple(line[1])], self.nodes[tuple(line[2])]
            if node_1.value == node_2.value == node_3.value and node_1.value is not None:
                return True
        return False

    def get_vulnerable_pieces(self):
        ret = []
        all_nodes = [node for (_, node) in self.nodes.items() if node.value == self.game.max_color]
        # if at most 3, all of them vulnerable
        if len(all_nodes) <= 3:
            return all_nodes
        for node in all_nodes:
            if not self.formed_line(node):
                ret += [node]
        return ret

    def capture_mode(self):
        vulnerable_pieces = self.get_vulnerable_pieces()
        for _, node in self.nodes.items():
            if node not in vulnerable_pieces:
                node.set_controller(DefaultController)
            else:
                node.set_controller(CaptureController)

    def capture(self, to_capture):
        for _, node in self.nodes.items():
            if node == to_capture:
                node.value = None
                return

    def handle_event(self, event):
        for _, node in self.nodes.items():
            node.handle_event(event)

    def update(self):
        for _, node in self.nodes.items():
            node.update()

    def render(self, screen):
        for board_coords, node in self.nodes.items():
            node.render(screen)