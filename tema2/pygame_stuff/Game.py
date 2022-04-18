import pygame

from . import EventManager
from .MinPlayer import MinPlayer
from .MaxPlayer import MaxPlayer
from .Graph import Graph
from .Node import Node
from .EventManager import EventManager

class Button:
    def __init__(self, button_group, coords, text, color='white', background_color='blue', selected_color='orange'):
        self.button_group = button_group
        self.coords = coords
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.txt = text
        self.text = self.font.render(text, True, pygame.Color(color))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (self.coords[0], self.coords[1] - 20)
        self.color = color
        self.background_color = background_color
        self.selected_color = selected_color
        self.selected = False

    def select(self):
        self.selected = True
        self.button_group.selected = self
        self.button_group.deselect_others(self)

    def handle_event(self, e):
        mp = pygame.mouse.get_pos()
        if e.type == pygame.MOUSEMOTION:
            if self.text_rect.collidepoint(mp):
                self.background_color = 'green'
            else:
                self.background_color = 'blue'
        if e.type == pygame.MOUSEBUTTONDOWN:
            if self.text_rect.collidepoint(mp):
                self.select()

    def update(self):
        pass

    def render(self, screen):
        pygame.draw.rect(screen, pygame.Color(self.background_color if not self.selected else self.selected_color), self.text_rect)
        screen.blit(self.text, self.text_rect)

class CallbackButton:
    def __init__(self, coords, text, callback = None, color='white', background_color='blue', selected_color='orange'):
        self.coords = coords
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.text = self.font.render(text, True, pygame.Color(color))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (self.coords[0], self.coords[1] - 20)
        self.color = color
        self.background_color = background_color
        self.selected_color = selected_color
        self.callback = callback

    def handle_event(self, e):
        mp = pygame.mouse.get_pos()
        if e.type == pygame.MOUSEMOTION:
            if self.text_rect.collidepoint(mp):
                self.background_color = 'green'
            else:
                self.background_color = 'blue'
        if e.type == pygame.MOUSEBUTTONDOWN:
            if self.text_rect.collidepoint(mp):
                if self.callback is not None:
                    self.callback()

    def update(self):
        pass

    def render(self, screen):
        pygame.draw.rect(screen, pygame.Color(self.background_color),
                         self.text_rect)
        screen.blit(self.text, self.text_rect)

class ButtonGroup:
    def __init__(self, text, coords):
        self.font = pygame.font.Font('freesansbold.ttf', 40)
        self.text = self.font.render(text, True, pygame.Color('black'))
        self.text_rect = self.text.get_rect()
        self.coords = coords
        self.text_rect.center = (self.coords[0], self.coords[1] - 20)

        self.buttons = []
        self.selected = None

    def set_first_selected(self):
        self.selected = self.buttons[0]
        self.buttons[0].selected = True

    def deselect_others(self, b):
        for button in self.buttons:
            if button == b:
                continue
            button.selected = False

    def add_button(self, b):
        self.buttons += [b]

    def handle_event(self, e):
        for b in self.buttons:
            b.handle_event(e)

    def render(self, screen):
        screen.blit(self.text, self.text_rect)
        for b in self.buttons:
            b.render(screen)


class OptionMenu:
    def __init__(self, game):
        self.game = game
        self.button_groups = []
        self.start_button = CallbackButton((200, 400), 'start', self.start)

    def start(self):
        self.game.min_color = self.button_groups[0].selected.txt
        self.game.max_color = 'black' if self.game.min_color == 'white' else 'white'
        self.game.max_strategy = self.button_groups[1].selected.txt
        self.game.difficulty = self.button_groups[2].selected.txt

        print(self.game.max_color, self.game.max_strategy, self.game.difficulty)
        self.game.option_menu = None

    def add_button_group(self, bg):
        self.button_groups += [bg]
        bg.set_first_selected()

    def update(self):
        pass

    def handle_event(self, e):
        for bg in self.button_groups:
            bg.handle_event(e)
        self.start_button.handle_event(e)

    def render(self, screen):
        self.start_button.render(screen)
        for bg in self.button_groups:
            bg.render(screen)

class Game:
    def __init__(self, screen_size):
        self.size = screen_size

        # self.max_color = 'black'
        # self.min_color = 'black' if self.max_color == 'white' else 'white'
        self.max_color = None
        self.min_color = None

        # self.max_strategy = 'min-max'
        # self.max_strategy = 'alpha-beta'
        self.max_strategy = None
        self.difficulty = None

        self.max_pieces = 6
        self.min_pieces = self.max_pieces

        self.padding = 40
        self.cell_size = (screen_size - self.padding * 2) / 6
        self.board_surface = pygame.Surface((self.size - 2*self.padding, self.size - 2*self.padding))
        self.board_surface.fill(pygame.Color("white"))

        self.graph = Graph(self)
        self.option_menu = OptionMenu(self)

        self.current_player = MinPlayer()

        EventManager.connect("next_turn", self.next_turn)
        EventManager.connect("end_game", self.end_game)
        self.setup()

    def jucator_opus(self, jucator):
        if jucator == self.max_color:
            return self.min_color
        else:
            return self.max_color

    def setup(self):
        color_bg = ButtonGroup('player color', (150, 50))
        color_bg.add_button(Button(color_bg, (350, 50), "black"))
        color_bg.add_button(Button(color_bg, (450, 50), "white"))
        self.option_menu.add_button_group(color_bg)

        color_bg = ButtonGroup('ai algorithm', (150, 150))
        color_bg.add_button(Button(color_bg, (350, 150), "min-max"))
        color_bg.add_button(Button(color_bg, (550, 150), "alpha-beta"))
        self.option_menu.add_button_group(color_bg)

        color_bg = ButtonGroup('dificultate', (150, 250))
        color_bg.add_button(Button(color_bg, (300, 250), "usor"))
        color_bg.add_button(Button(color_bg, (400, 250), "mediu"))
        color_bg.add_button(Button(color_bg, (500, 250), "greu"))
        self.option_menu.add_button_group(color_bg)

    def end_game(self, winning_player, *args):
        print("GAME ENDED WINNER")
        print(winning_player)

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                self.next_turn()

        if self.option_menu is not None:
            self.option_menu.handle_event(event)
        else:
            self.graph.handle_event(event)

    def next_turn(self, *args):
        print("next turn")
        if isinstance(self.current_player, MinPlayer):
            self.current_player = MaxPlayer(self)
        else:
            self.current_player = MinPlayer()

        self.current_player.play_turn()

    def update(self):
        if self.option_menu is not None:
            self.option_menu.update()
        else:
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
        if self.option_menu is not None:
            self.option_menu.render(screen)
        else:
            self.draw_board(screen)
            self.graph.render(screen)
