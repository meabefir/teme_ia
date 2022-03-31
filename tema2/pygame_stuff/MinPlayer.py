import pygame
from .EventManager import EventManager

class MinPlayer:
    def __init__(self):
        print("PLAYER turn")

        EventManager.emit_signal("min_turn")

    def play_turn(self):
        pass