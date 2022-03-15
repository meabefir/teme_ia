import pygame
from .Cell import Cell
from .ColorPicker import ColorPicker
from .Piece import Piece
from .PieceMove import PieceMove

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

    def mocAnimate(self):
        self.moves.append(PieceMove(self, 'red', 'e', 20))
        self.moves.append(PieceMove(self, 'red', 'e', 20))
        self.moves.append(PieceMove(self, 'red', 'e', 20))
        self.moves.append(PieceMove(self, 'red', 's', 20))
        self.moves.append(PieceMove(self, 'red', 's', 20))
        self.moves.append(PieceMove(self, 'red', 'w', 20))
        self.moves.append(PieceMove(self, 'red', 'w', 20))
        self.moves.append(PieceMove(self, 'red', 'w', 20))
        self.moves.append(PieceMove(self, 'red', 's', 20))
        self.moves.append(PieceMove(self, 'red', 'n', 20))
        self.moves.append(PieceMove(self, 'red', 'n', 20))
        self.animating = True

    def setSelectedColor(self, color):
        self.selectedColor = color

    def isBorderBlock(self, row, col):
        return row == 0 or col == 0 or row == self.rows - 1 or col == self.cols - 1

    def serialize(self):
        str = ""
        current_char = 'a'
        dic = {}
        for l_row in self.data:
            str += '\n'
            for cell in l_row:
                if cell.value == 'red':
                    str += '*'
                elif cell.value in ['.', '#']:
                    str += cell.value
                else:
                    if cell.value in dic:
                        str += dic[cell.value]
                    else:
                        dic[cell.value] = current_char
                        current_char = chr(ord(current_char)+1)
                        str += dic[cell.value]
        return str

    def removePiece(self, value):
        self.pieces.pop(value, None)

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
                    if left:
                        # daca nu este mouse-ul peste ea
                        if not cell.isMouseOver():
                            continue

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

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                print(self.serialize())
            elif event.key == pygame.K_p:
                print(self.pieces)
            elif event.key == pygame.K_a:
                self.mocAnimate()

    def update(self):
        if len(self.moves):
            self.moves[0].update()
            if self.moves[0].finished:
                self.moves.pop(0)
                if len(self.moves) == 0:
                    self.animating = False

    def draw_cell_borders(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                pygame.draw.rect(screen, pygame.Color("white"), (self.rect.y + col * self.cell_size, self.rect.x + row * self.cell_size, self.cell_size, self.cell_size), 1)

    def render(self, screen):
        pygame.draw.rect(screen, ColorPicker.COLORS[self.selectedColor], self.rect, 2)

        self.draw_cell_borders(screen)

        for row in self.data:
            for cell in row:
                cell.render(screen)