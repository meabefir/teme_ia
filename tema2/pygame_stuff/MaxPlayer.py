import pygame
import random

from .EventManager import EventManager

class MaxPlayer:
    def __init__(self, game):
        print("AI turn")
        self.game = game

        EventManager.emit_signal("max_turn")

    def play_turn(self):
        # nodes = []
        # for _, node in self.game.graph.nodes.items():
        #     if node.value is None:
        #         nodes += [node]
        # if len(nodes) == 0:
        #     return
        # random_node = random.choice(nodes)
        # print(random_node)
        # random_node.value = self.game.max_color
        # print(random_node)
        #
        # self.game.next_turn()
        EventManager.emit_signal("next_turn")
        pass
