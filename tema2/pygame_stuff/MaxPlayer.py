import pygame
import random

from .EventManager import EventManager
from .node_controllers.MovingController import MovingController
from .Graph import PiecePlacement, PieceMove

class MaxPlayer:
    def __init__(self, game):
        print("AI turn")
        self.game = game

        EventManager.emit_signal("max_turn")

    def play_turn(self):

        if self.game.max_strategy == "test":
            if self.game.max_pieces == 0:
                self.move_random_piece()
            else:
                self.place_random_piece()
        elif self.game.max_strategy == "min-max":
            stare_start = Stare(self.game.graph, self.game.max_color, 2, self.game)

            outcome = self.min_max(stare_start)
            print("\n\n\nAICI")
            print(outcome)
            last_move = outcome.stare_aleasa.tabla_joc.last_move
            print(last_move)
            nodes = self.game.graph.nodes
            if isinstance(last_move, PiecePlacement):
                nodes[last_move.from_coords].value = self.game.max_color
                self.game.graph.max_pieces -= 1
                if last_move.taken_coords is not None:
                    nodes[last_move.taken_coords].value = None
                EventManager.emit_signal("next_turn")
            elif isinstance(last_move, PieceMove):
                nodes[last_move.from_coords].set_controller(MovingController, nodes[last_move.to_coords], nodes[last_move.taken_coords] if last_move.taken_coords is not None else None)
                # node.set_controller(MovingController, neigh, to_capture)

            # print(outcome.tabla_joc.last_move)

        return
        # check what ai to use, min-max or alpha beta

        # build the search tree

        graph = self.game.graph
        min_pieces = [node for node in graph.nodes.values() if node.value == self.game.min_color]

        # # muta o piesa random si daca a facut linie, captureaza o piesa random
        # for _, node in graph.nodes.items():
        #     if node.value == self.game.max_color and node.can_move():
        #         for neigh in node.neighs:
        #             if neigh.value is None:
        #                 # move to that node
        #                 to_capture = random.choice(min_pieces)
        #                 node.set_controller(MovingController, neigh, to_capture)
        #                 return
        # plaseaza o piesa random
        for node in graph.nodes.values():
            if node.value is None:
                if self.game.max_pieces > 0:
                    self.game.max_pieces -= 1
                    node.value = self.game.max_color
                    break

        # aici nu a gasit nici o piesa de mutat
        # stc

        EventManager.emit_signal("next_turn")
        pass

    def place_random_piece(self):
        graph = self.game.graph
        for node in graph.nodes.values():
            if node.value is None:
                if self.game.max_pieces > 0:
                    self.game.max_pieces -= 1
                    node.value = self.game.max_color
                    break
        EventManager.emit_signal("next_turn")

    def move_random_piece(self):
        graph = self.game.graph
        min_pieces = [node for node in graph.nodes.values() if node.value == self.game.min_color]

        # muta o piesa random si daca a facut linie, captureaza o piesa random
        for _, node in graph.nodes.items():
            if node.value == self.game.max_color and node.can_move():
                for neigh in node.neighs:
                    if neigh.value is None:
                        # move to that node
                        to_capture = random.choice(min_pieces)
                        node.set_controller(MovingController, neigh, to_capture)
                        return
        EventManager.emit_signal("next_turn")


    def min_max(self, stare):
        # if stare.adancime == 0 or stare.tabla_joc.final():
        if stare.adancime == 0:
            stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
            return stare

        # calculez toate mutarile posibile din starea curenta
        stare.mutari_posibile = stare.mutari()

        # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
        mutariCuEstimare = [self.min_max(mutare) for mutare in stare.mutari_posibile]

        if stare.j_curent == self.game.max_color:
            # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
            stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
        else:
            # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
            stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)
        stare.estimare = stare.stare_aleasa.estimare
        return stare


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
    """

    def __init__(self, tabla_joc, j_curent, adancime, game, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent
        self.game = game

        # adancimea in arborele de stari
        self.adancime = adancime

        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = self.game.jucator_opus(self.j_curent)
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, self.game, parinte=self) for mutare in l_mutari]

        return l_stari_mutari
