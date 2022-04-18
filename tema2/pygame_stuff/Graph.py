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
    def __init__(self, game, nodes=None, last_move=None, max_pieces=None, min_pieces=None):
        self.game = game

        self.nodes = nodes if nodes is not None else {}
        self.lines = self.read_lines()
        self.last_move = last_move

        self.max_pieces = max_pieces if max_pieces is not None else self.game.max_pieces
        self.min_pieces = min_pieces if min_pieces is not None else self.game.min_pieces

        # print("MAX PIECES")
        # print(self.max_pieces)

        if self.nodes == {}:
            self.setup()

        # print(self.nodes)

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
        # pprint(data)
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
            # if random.random() < .4:
            #     color = random.choice(colors)
            #     if color == self.game.min_color:
            #         if self.game.min_pieces == 0:
            #             color = None
            #         else:
            #             self.game.min_pieces -= 1
            #     elif color == self.game.max_color:
            #         if self.game.max_pieces == 0:
            #             color = None
            #         else:
            #             self.game.max_pieces -= 1

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

    def formed_line(self, node, nodes=None):
        if node.value is None:
            return False
        if nodes is None:
            nodes = self.nodes
        node_board_coords = node.board_coords
        for line in self.lines:
            if list(node_board_coords) not in line:
                continue
            node_1, node_2, node_3 = nodes[tuple(line[0])], nodes[tuple(line[1])], nodes[tuple(line[2])]
            if node_1.value == node_2.value == node_3.value and node_1.value is not None:
                return True
        return False

    # stc add color option
    def get_vulnerable_pieces(self, color=None, nodes=None):
        if nodes is None:
            nodes = self.nodes
        if color is None:
            color = self.game.max_color
        ret = []
        all_nodes = [node for (_, node) in self.nodes.items() if node.value == color]
        # if at most 3, all of them vulnerable
        if len(all_nodes) <= 3:
            return all_nodes
        for node in all_nodes:
            if not self.formed_line(node, nodes):
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
                to_capture_color = node.value
                node.value = None
                # verific daca era ultimul nod de acea culoare si daca jucatorul respectiv nu mai are piese de pus
                found = False
                for node in self.nodes.values():
                    if node.value == to_capture_color:
                        found = True
                        break
                if not found:
                    # verific daca mai sunt piese de culoare aia
                    if to_capture_color == self.game.max_color:
                        if self.game.max_pieces == 0:
                            EventManager.emit_signal("end_game", self.game.max_color)
                            return
                    elif to_capture_color == self.game.min_color:
                        if self.game.min_pieces == 0:
                            EventManager.emit_signal("end_game", self.game.min_color)
                            return
                # aici inseamna ca mai sunt piese de eliminat si vine next turn
                EventManager.emit_signal("next_turn")
                return
        EventManager.emit_signal("next_turn")

    def estimeaza_scor(self, adancime):
        points = 0

        points += self.max_pieces
        points += self.min_pieces

        for node in self.nodes.values():
            if node.value == self.game.max_color:
                points += 1
            elif node.value == self.game.min_color:
                points -= 1

        return points

    def copy_nodes(self, nodes):
        ret = {}

        for node in nodes.values():
            ret[node.board_coords] = Node(node.game, None, node.board_coords, (-100, -100), node.value)

        # set the graph for all the nodes!! or not

        return ret

    def mutari(self, current_player):
        ret = []

        # mutari de placing
        pieces_left = self.max_pieces if current_player == self.game.max_color else self.min_pieces
        if pieces_left > 0:
            for key, node in self.nodes.items():
                if node.value is None:
                    # nodes_cpy = copy.deepcopy(self.nodes)
                    nodes_cpy = self.copy_nodes(self.nodes)
                    nodes_cpy[key].value = current_player
                    # verific daca a format linie, daca da, elimin din piesele jucatorului min
                    if self.formed_line(nodes_cpy[key], nodes_cpy):
                        # print(nodes_cpy[key], ' a facut linie')
                        pieces_to_capture = self.get_vulnerable_pieces(self.game.jucator_opus(current_player))
                        # adauga mutare si daca nu exista piese de capturat
                        for piece in pieces_to_capture:
                            # nodes_cpyy = copy.deepcopy(nodes_cpy)
                            nodes_cpyy = self.copy_nodes(nodes_cpy)
                            nodes_cpyy[piece.board_coords].value = None

                            ret += [Graph(self.game, nodes_cpyy,
                                          PiecePlacement(nodes_cpy[key].board_coords, piece.board_coords),
                                          self.max_pieces - 1 if current_player == self.game.max_color else self.max_pieces,
                                          self.min_pieces - 1 if current_player == self.game.min_color else self.min_pieces)]
                    else:
                        ret += [Graph(self.game, nodes_cpy, PiecePlacement(nodes_cpy[key].board_coords, None),
                                      self.max_pieces - 1 if current_player == self.game.max_color else self.max_pieces,
                                      self.min_pieces - 1 if current_player == self.game.min_color else self.min_pieces)]

        # mutari de mutare
        for key, node in self.nodes.items():
            if node.value == current_player:
                for neigh in node.neighs:
                    if neigh.value is None:
                        # il mutam la vecin (in copie)
                        # nodes_cpy = copy.deepcopy(self.nodes)
                        nodes_cpy = self.copy_nodes(self.nodes)
                        # fac switch
                        nodes_cpy[key].value = None
                        nodes_cpy[neigh.board_coords].value = current_player

                        # verific daca a format linie, daca da, elimin din piesele jucatorului min
                        if self.formed_line(nodes_cpy[neigh.board_coords], nodes_cpy):
                            pieces_to_capture = self.get_vulnerable_pieces(self.game.jucator_opus(current_player))
                            for piece in pieces_to_capture:
                                nodes_cpyy = self.copy_nodes(nodes_cpy)
                                nodes_cpyy[piece.board_coords].value = None

                                ret += [Graph(self.game, nodes_cpyy,
                                              PieceMove(nodes_cpy[key].board_coords, neigh.board_coords,
                                                        piece.board_coords),
                                              self.max_pieces,
                                              self.min_pieces)]
                        else:
                            ret += [Graph(self.game, nodes_cpy,
                                          PieceMove(nodes_cpy[key].board_coords, neigh.board_coords, None),
                                          self.max_pieces,
                                          self.min_pieces)]
        print(f's-au gasit {len(ret)} mutari posibile')
        return ret
        # to implement

    def handle_event(self, event):
        for _, node in self.nodes.items():
            node.handle_event(event)

    def update(self):
        for _, node in self.nodes.items():
            node.update()

    def render(self, screen):
        for board_coords, node in self.nodes.items():
            node.render(screen)


class PiecePlacement():
    def __init__(self, from_coords, taken_coords):
        self.from_coords = from_coords
        self.taken_coords = taken_coords

    def __str__(self):
        return f"piece place {self.from_coords} take {self.taken_coords}"


class PieceMove():
    def __init__(self, from_coords, to_coords, taken_coords):
        self.from_coords = from_coords
        self.to_coords = to_coords
        self.taken_coords = taken_coords

    def __str__(self):
        return f"piece move {self.from_coords} to {self.to_coords} take {self.taken_coords}"
