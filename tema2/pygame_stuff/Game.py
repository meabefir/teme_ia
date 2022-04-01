import pygame

from . import EventManager
from .MinPlayer import MinPlayer
from .MaxPlayer import MaxPlayer
from .Graph import Graph
from .Node import Node
from .EventManager import EventManager

class Game:
    def __init__(self, screen_size):
        self.size = screen_size

        self.max_color = 'black'
        self.min_color = 'black' if self.max_color == 'white' else 'white'

        self.max_pieces = 12
        self.min_pieces = 12

        self.padding = 40
        self.cell_size = (screen_size - self.padding * 2) / 6
        self.board_surface = pygame.Surface((self.size - 2*self.padding, self.size - 2*self.padding))
        self.board_surface.fill(pygame.Color("white"))

        self.graph = Graph(self)

        self.current_player = MinPlayer()

        EventManager.connect("next_turn", self.next_turn)
        # self.setup()

    def setup(self):
        pass

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                self.next_turn()

        self.graph.handle_event(event)

    def next_turn(self, *args):
        print("next turn")
        if isinstance(self.current_player, MinPlayer):
            self.current_player = MaxPlayer(self)
        else:
            self.current_player = MinPlayer()

        self.current_player.play_turn()

    def update(self):
        self.graph.update()

    def draw_board(self, screen):
        line_color = pygame.Color("black")

        # horizontal lines
        self.draw_board_line(screen, line_color, (0, 0), (6, 0))
        self.draw_board_line(screen, line_color, (1, 1), (5, 1))
        self.draw_board_line(screen, line_color, (2, 2), (4, 2))
        self.draw_board_line(screen, line_color, (2, 4), (4, 4))
        self.draw_board_line(screen, line_color, (1, 5), (5, 5))
        self.draw_board_line(screen, line_color, (0, 6), (6, 6))
        self.draw_board_line(screen, line_color, (0, 3), (2, 3))
        self.draw_board_line(screen, line_color, (4, 3), (6, 3))

        # vertical lines
        self.draw_board_line(screen, line_color, (0, 0), (0, 6))
        self.draw_board_line(screen, line_color, (1, 1), (1, 5))
        self.draw_board_line(screen, line_color, (2, 2), (2, 4))
        self.draw_board_line(screen, line_color, (4, 2), (4, 4))
        self.draw_board_line(screen, line_color, (5, 1), (5, 5))
        self.draw_board_line(screen, line_color, (6, 0), (6, 6))
        self.draw_board_line(screen, line_color, (3, 0), (3, 2))
        self.draw_board_line(screen, line_color, (3, 4), (3, 6))

        # horizontal lines
        self.draw_board_line(screen, line_color, (0, 0), (2, 2))
        self.draw_board_line(screen, line_color, (6, 0), (4, 2))
        self.draw_board_line(screen, line_color, (0, 6), (2, 4))
        self.draw_board_line(screen, line_color, (4, 4), (6, 6))

        # pygame.Surface.blit(tmp_surface, screen, (self.padding, self.padding))

    def draw_board_line(self, screen, color, start, end):
        pygame.draw.line(screen, color, (start[0] * self.cell_size + self.padding, start[1] * self.cell_size + self.padding),
                                      (end[0] * self.cell_size + self.padding, end[1] * self.cell_size + self.padding), 3)

    def render(self, screen):
        self.draw_board(screen)
        self.graph.render(screen)
