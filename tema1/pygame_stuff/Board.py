import pygame
import threading
from .Cell import Cell
from .ColorPicker import ColorPicker
from .Piece import Piece
from .PieceMove import PieceMove
from .pygame_wrapper import draw_rect

from classes import Graph
from astar import a_star
from astar_opt import a_star_opt
from astar_opti import a_star_opti
from idastar import ida_star_noprint
from dfs import dfs
from bfs import bfs
from dfi import dfi

class Board:
    def __init__(self, pos, rows, cols, width=200):
        self.cell_size = width / cols
        height = self.cell_size * rows
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.rows = rows
        self.cols = cols
        self.data = [[None for col in range(cols)] for row in range(rows)]
        self.pieces = {}

        self.selectedColor = None

        self.moves = []
        self.animating = False

        # init middle content
        for row in range(1, self.rows-1):
            for col in range(1, self.cols-1):
                self.data[row][col] = Cell(".", row, col, (self.rect.x + col * self.cell_size, self.rect.y + row * self.cell_size), self.cell_size)

        # init borders with solid block
        for col in range(self.cols):
            self.data[0][col] = Cell("#", 0, col, (self.rect.x + col * self.cell_size, self.rect.y + 0 * self.cell_size), self.cell_size)
            self.data[self.rows-1][col] = Cell("#", self.rows-1, col, (self.rect.x + col * self.cell_size, self.rect.y + (self.rows-1) * self.cell_size), self.cell_size)
        for row in range(1, self.rows-1):
            self.data[row][0] = Cell("#", row, 0, (self.rect.x + 0 * self.cell_size, self.rect.y + row * self.cell_size), self.cell_size)
            self.data[row][self.cols-1] = Cell("#", row, self.cols-1, (self.rect.x + (self.cols-1) * self.cell_size, self.rect.y + row * self.cell_size), self.cell_size)

    def loadFromString(self, s):
        colors_used = {'*': 'red'}
        self.pieces['red'] = Piece(self, 'red')
        for row, line in enumerate(s):
            for col, ch in enumerate(line):
                if ch in ['.', '#']:
                    self.data[row][col].value = ch
                    continue
                # set color for this char
                if ch not in colors_used:
                    for color in ColorPicker.COLORS:
                        if color in colors_used.values():
                            continue
                        colors_used[ch] = color
                        break

                self.data[row][col].value = colors_used[ch]
                if colors_used[ch] not in self.pieces:
                    self.pieces[colors_used[ch]] = Piece(self, colors_used[ch])
                self.pieces[colors_used[ch]].addBlock(row, col)

        print(self.pieces)

    def animate(self):
        self.animating = True

    def stopAnimate(self):
        self.animating = False

    def mocAnimate(self):
        # self.moves.append(PieceMove(self, self.pieces["red"], 'e', 20))
        # self.moves.append(PieceMove(self, self.pieces["red"], 's', 20))
        # self.moves.append(PieceMove(self, self.pieces["red"], 'w', 20))
        # self.moves.append(PieceMove(self, self.pieces["red"], 's', 20))
        # self.moves.append(PieceMove(self, self.pieces["red"], 'e', 20))
        # self.moves.append(PieceMove(self, self.pieces["red"], 'n', 20))
        # self.moves.append(PieceMove(self, self.pieces["red"], 'w', 20))
        # self.moves.append(PieceMove(self, self.pieces["red"], 'n', 20))

        self.moves.append(PieceMove(self, self.pieces["red"], 's', 20))

        self.animate()

    def setSelectedColor(self, color):
        self.selectedColor = color

    def isBorderBlock(self, row, col):
        return row == 0 or col == 0 or row == self.rows - 1 or col == self.cols - 1

    def serialize(self):
        str = ""
        current_char = 'a'
        dic = {}
        for i, l_row in enumerate(self.data):
            for cell in l_row:
                if cell.value == 'red':
                    str += '*'
                    dic['red'] = '*'
                elif cell.value in ['.', '#']:
                    str += cell.value
                else:
                    if cell.value in dic:
                        str += dic[cell.value]
                    else:
                        dic[cell.value] = current_char
                        current_char = chr(ord(current_char)+1)
                        str += dic[cell.value]
            if i == len(self.data) - 1:
                continue
            str += '\n'
        return str, dic

    def removePiece(self, value):
        self.pieces.pop(value, None)

    def inBounds(self, row, col):
        return 0 <= row < len(self.data) and 0 <= col < len(self.data[0])

    def attemptPieceMove(self, key):
        key_dir_map = {
            pygame.K_UP: 'n',
            pygame.K_DOWN: 's',
            pygame.K_LEFT: 'w',
            pygame.K_RIGHT: 'e'
        }

        for l_row in self.data:
            for cell in l_row:
                if cell.isMouseOver():
                    if cell.value in ['.', '#']:
                        return
                    self.moves.append(PieceMove(self, self.pieces[cell.value], key_dir_map[key], 20))
                    self.animate()
                    return

    def findSolution(self):
        s, dic = self.serialize()
        if 'red' not in dic:
            return

        rev_dic = {'*': 'red'}
        for key, val in dic.items():
            rev_dic[val] = key
        graph = Graph(None, s)

        _timeout = 5
        # moves = bfs(graph, 1, timeout=_timeout)
        # moves = dfs(graph, 1, timeout=_timeout)
        # moves = dfi(graph, 1, timeout=_timeout)
        moves = a_star(graph, 1, "euristica admisibila 1", timeout=_timeout)
        # moves = a_star_opt(graph, 1, "euristica admisibila 1", timeout=_timeout)
        # moves = ida_star_noprint(graph, 1, "euristica admisibila 1", timeout=_timeout)

        print("moves ", moves)
        if not moves:
            return
        if isinstance(moves, str):
            return
        for move in moves:
            self.moves.append(PieceMove(self, self.pieces[rev_dic[move[0]]], move[1], 3))
        self.animate()

    def handleEvent(self, event):
        if self.animating:
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            # left clicked
            left, middle, right = pygame.mouse.get_pressed()

            if self.selectedColor is None:
                return
            for row, l_row in enumerate(self.data):
                for col, cell in enumerate(l_row):
                    if not cell.isMouseOver():
                        continue
                    if left:
                        # daca e celula margine nu ii pot da culoare
                        if self.isBorderBlock(row, col):
                            if cell.value == '#':
                                cell.assignValue('.')
                            else:
                                cell.assignValue('#')
                            return

                        # daca apas pe ea cu aceeasi culoare o elimin
                        # trb sa fiu atent sa nu se separe blocurile
                        if cell.value == self.selectedColor:
                            if self.pieces[self.selectedColor].splitsIfRemove(row, col):
                                return
                            self.pieces[self.selectedColor].removeBlock(row, col)
                            cell.assignValue('.')
                            return

                        # daca apas pe un spatiu gol sau pe un spatiu de alta culoare

                        # daca este deja ocupat si punand alta culoare acolo le separam piesa originala
                        if cell.value != '.':
                            if self.pieces[cell.value].splitsIfRemove(row, col):
                                return

                        # verific sa fie vecin cu culoarea asta, nu pot sa incep un bloc nou de aceeasi culoare separat de originalul
                        if self.selectedColor in self.pieces:
                            if not self.pieces[self.selectedColor].neighOf(row, col):
                                return
                        # daca am verificat si este vecin, ii dam culoarea si il unim cu piesa, dar mai intai verific daca deja avea culoare ca sa o elimin din piesa ei
                        if cell.value != '.':
                            self.pieces[cell.value].removeBlock(row, col)
                        cell.assignValue(self.selectedColor)
                        if self.selectedColor in self.pieces:
                            self.pieces[self.selectedColor].addBlock(row, col)
                        else:
                            new_piece = Piece(self, self.selectedColor)
                            new_piece.addBlock(row, col)
                            self.pieces[self.selectedColor] = new_piece
                    elif right:
                        if cell.value not in ['.', '*', '#']:
                            if not self.pieces[cell.value].splitsIfRemove(row, col):
                                self.pieces[cell.value].removeBlock(row, col)
                                cell.assignValue('.')

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                print(self.serialize()[0])
            elif event.key == pygame.K_p:
                print(self.pieces)
            elif event.key == pygame.K_a:
                self.mocAnimate()
            elif event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                self.attemptPieceMove(event.key)
            elif event.key == pygame.K_f:
                self.findSolution()

    def update(self):
        # only update the first animation given
        if self.animating:
            if len(self.moves):
                # check if can move that piece
                if self.moves[0].started == False:
                    if not self.moves[0].piece.canMoveTo(self.moves[0].dir):
                        self.moves.pop(0)
                        if len(self.moves) == 0:
                            self.stopAnimate()
                        return
                    self.moves[0].start()
                    return

                self.moves[0].update()
                if self.moves[0].finished:
                    self.moves.pop(0)
                    if len(self.moves) == 0:
                        self.stopAnimate()

    def draw_cell_borders(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                draw_rect(screen, pygame.Color("white"),
                          pygame.Rect(self.rect.y + col * self.cell_size,
                                      self.rect.x + row * self.cell_size,
                                      self.cell_size, self.cell_size), 1)
                # pygame.draw.rect(screen, pygame.Color("white"), (self.rect.y + col * self.cell_size, self.rect.x + row * self.cell_size, self.cell_size, self.cell_size), 1)

    def render(self, screen):
        pygame.draw.rect(screen, ColorPicker.COLORS[self.selectedColor], self.rect, 5)

        self.draw_cell_borders(screen)

        for row in self.data:
            for cell in row:
                cell.render(screen)