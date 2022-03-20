import copy
from pprint import pprint

class Piece:
    """
        Clasa care incapsuleaza o piesa de pe tabla

            board = matricea tablei de joc
            blocks = blocurile din care e formata
            name = simbolul
        """
    def __init__(self, board, blocks, name):
        self.board = board
        self.blocks = blocks
        self.name = name

        self.reset()

    def reset(self):
        """
            reseteaza "cutia" in care se afla piesa
        """
        self.bbrow1 = min([el[0] for el in self.blocks])
        self.bbrow2 = max([el[0] for el in self.blocks])
        self.bbcol1 = min([el[1] for el in self.blocks])
        self.bbcol2 = max([el[1] for el in self.blocks])

    def getBBString(self):
        # just for testing
        ret = f'{self.bbrow1} {self.bbcol1} {self.bbrow2} {self.bbcol2}'
        return ret

    def getBB(self):
        """
    Returns:
        coordonatele "cutiei" in care se incadreaza piesa
    """
        return self.bbrow1, self.bbcol1, self.bbrow2, self.bbcol2

    def getCost(self):
        """
            Returns:
                costul de a misca piesa
            """
        if self.name == '*':
            return 1
        return len(self.blocks)

    def move(self, dir):
        """
            functie care muta piesa intr-o anumita directie
            Args:
                dir: directia in care sa se mute piesa
            Returns:
                un nou obiect Piece care este mutat in directia ceruta
            """
        d_row, d_col = 0, 0
        if (dir == 's'):
            d_row = 1
        elif (dir == 'n'):
            d_row = -1
        elif (dir == 'w'):
            d_col = -1
        elif (dir == 'e'):
            d_col = 1
        new_blocks = []
        for block in self.blocks:
            new_blocks.append((block[0] + d_row, block[1] + d_col))
        return Piece(self.board, new_blocks, self.name)

    def isOOB(self):
        """
            verifica daca "cutia" in care se incadreaza piesa a ajuns in afara tablei
            """
        return self.bbrow2 < 0 or self.bbrow1 >= len(self.board) or self.bbcol2 < 0 or self.bbcol1 >= len(self.board[0])

    def __str__(self):
        ret = f'[{self.name}]\n'

        # for block in self.blocks:
        # 	ret += "(" + str(block[0]) + ", " + str(block[1]) + ") "
        # ret += '\n'

        str_mat = [['.' for _ in range(self.bbcol2 - self.bbcol1 + 1 + 2)] for _ in
                   range(self.bbrow2 - self.bbrow1 + 1 + 2)]
        for block in self.blocks:
            str_mat[block[0] - self.bbrow1 + 1][block[1] - self.bbcol1 + 1] = self.name
        for line in str_mat:
            ret += "".join(line)
            ret += "\n"
        return ret


drow = [-1, 0, 1, 0]
dcol = [0, 1, 0, -1]


# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    def __init__(self, board, parinte, info={}, cost=0, h=0, dir=None, movedPiece=None, numar_ordine = 0):
        # matrice care tine tabla
        self.board = board
        self.numar_ordine = numar_ordine
        self.setTuple()
        self.str = self.setStr()
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost  # consider cost=1 pentru o mutare
        self.h = h
        self.dir = dir
        self.movedPiece = movedPiece
        self.f = self.g + self.h
        # dictionar de Piece care tine pozitiile unei piese
        self.info = info

        if self.info != {}:
            return

        dic_piese = {}
        visited = [[False for _ in range(len(self.board[0]))] for _ in range(len(self.board))]
        for (row, line) in enumerate(self.board):
            for (col, el) in enumerate(line):
                if el in dic_piese or el == "#" or el == ".":
                    continue
                # am intalnit o piesa pe care nu am construit-o inca
                dic_piese[el] = True
                self.buildPiece(row, col, visited)

    def setTuple(self):
        self.tup = (tuple(row) for row in self.board)

    def buildPiece(self, row, col, visited):
        """
            construieste o piesa noua din blocul care se afla la coord row, col

            args:
                visited: ce elemente din matrice au fost vizitate deja
                row, col: coordonatele blocului pt care construim piesa
            """
        el = self.board[row][col]
        q = [(row, col)]
        blocks = []
        while len(q):
            curr_row, curr_col = q.pop()
            visited[curr_row][curr_col] = True
            blocks.append([curr_row, curr_col])
            for i in range(4):
                next_row, next_col = curr_row + drow[i], curr_col + dcol[i]
                # if in bounds
                if not (0 <= next_row < len(visited) and 0 <= next_col < len(visited[0])):
                    continue
                # if not visited
                if visited[next_row][next_col] is True:
                    continue
                # if same element
                if self.board[next_row][next_col] != el:
                    continue
                q.append((next_row, next_col))

        self.info[el] = Piece(self.board, blocks, el)

    def canMovePiece(self, piece, dir):
        """
            verifica si returneaza daca piesa "piece" poate fi mutata in directia "dir"
            acum cand scriu asta imi dau seama ca trebuia pusa in clasa Piece
            """
        d_row, d_col = 0, 0
        if (dir == 's'):
            d_row = 1
        elif (dir == 'n'):
            d_row = -1
        elif (dir == 'w'):
            d_col = -1
        elif (dir == 'e'):
            d_col = 1

        for block in piece.blocks:
            new_row, new_col = block[0] + d_row, block[1] + d_col
            if piece.name == '*':
                # daca a trecut de margini, trebuit lasat sa treaca
                if not (0 <= new_row < len(self.board) and 0 <= new_col < len(self.board[0])):
                    continue
                # altfel, la fel ca cele normale, sa nu poata trece prin pereti sau prin alte piese
                # asta e duplicat cu ala de mai jos dar momentan csf ncsf
                if self.board[new_row][new_col] == '#':
                    return False
                if self.board[new_row][new_col] != '.' and self.board[new_row][new_col] != piece.name:
                    return False
            else:
                if not (0 <= new_row < len(self.board) and 0 <= new_col < len(self.board[0])):
                    return False
                if self.board[new_row][new_col] == '#':
                    return False
                if self.board[new_row][new_col] != '.' and self.board[new_row][new_col] != piece.name:
                    return False
        return True

    def movePiece(self, piece, dir):
        """
            muta piesa piece in directia dir
            """
        d_row, d_col = 0, 0
        if dir == 's':
            d_row = 1
        elif dir == 'n':
            d_row = -1
        elif dir == 'w':
            d_col = -1
        elif dir == 'e':
            d_col = 1
        info_copy = copy.deepcopy(self.info)
        # for block in piece.blocks:
        for block in info_copy[piece.name].blocks:
            block[0] += d_row
            block[1] += d_col
        info_copy[piece.name].reset()

        board_copy = copy.deepcopy(self.board)
        for block in piece.blocks:
            if 0 <= block[0] < len(self.board) and 0 <= block[1] < len(self.board[0]):
                board_copy[block[0]][block[1]] = '.'
        # for block in piece.blocks:
        for block in info_copy[piece.name].blocks:
            if 0 <= block[0] < len(self.board) and 0 <= block[1] < len(self.board[0]):
                board_copy[block[0]][block[1]] = piece.name

        return board_copy, info_copy

    def setStr(self):
        ret = ""
        for row in self.board:
            str_row = ""
            for ch in row:
                str_row += ch
            str_row += '\n'
            ret += str_row
        return ret

    def isScope(self):
        """
            functia de verificare scop
            piesa speciala sa fie "out of bounds"
            """
        return self.info['*'].isOOB()

    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def getSolutionMoves(self):
        # returneaza mutarile intr-un format care poate fi inteles de implementarea grafica a problemei
        ret = []
        l = self.obtineDrum()
        for nod in l:
            if nod.movedPiece is None:
                continue
            ret += [[nod.movedPiece, nod.dir]]
        return ret

    def strAfisDrum(self, afisCost=True, afisLung=True):
        # folosita pt scriere in fisier
        l = self.obtineDrum()
        ret = ""
        if afisCost:
            ret += "Cost: " + str(self.g) + "\n"
        if afisCost:
            ret += "Lungime: " + str(len(l)) + "\n"
        for nod in l:
            ret += str(nod) + "\n"

        return ret

    def afisDrum(self, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        for nod in l:
            print(str(nod))
        if afisCost:
            print("Cost: ", self.g)
        if afisCost:
            print("Lungime: ", len(l))
        return len(l)

    def afisLungimeDrum(self):
        print(len(self.obtineDrum()))

    def contineInDrum(self, new_board):
        nodDrum = self
        while nodDrum is not None:
            if new_board == nodDrum.board:
                return True
            nodDrum = nodDrum.parinte

        return False

    def __hash__(self):
        return hash(self.str)

    def __repr__(self):
        sir = ""
        sir += str(self.board)
        return (sir)

    def __eq__(self, other):
        # return self.board == other.board
        return hash(self) == hash(other)

    def __lt__(self, other):
        if self.f < other.f:
            return True
        else:
            if self.g > other.g:
                return True
        return False

    def __str__(self):
        dir_map = {
            's': 'v', 'n': '^', 'w': '<', 'e': '>'
        }
        ret = ""
        if self.movedPiece is not None:
            ret += f'Moved {self.movedPiece} to {dir_map[self.dir]}\n'
        ret += "h: " + str(self.h) + "\n"
        ret += f"numar ordine: {self.numar_ordine}\n"
        ret += self.str + "\n"
        # for (key, value) in self.info.items():
        # 	ret += str(value)
        return ret


class Graph:  # graful problemei
    def __init__(self, nume_fisier, s=""):
        self.coordsExit = []
        self.noduri_generate = 1
        self.noduri_maxim = 0

        # daca primeste nume de fisier, citeste din acesta, altfel primeste un string input (folosit in partea grafica)
        continutFisier = ""
        if nume_fisier is not None:
            f = open(nume_fisier, 'r')
            continutFisier = f.read()
            f.close()
        else:
            continutFisier = s


        self.start = [[el for el in line] for line in continutFisier.split("\n")]

        # pastrez coordonatele pe unde se poate iesi
        # caut pe borduri unde e portita
        for i in range(len(self.start[0])):
            if self.start[0][i] == '.':
                self.coordsExit += [[0, i]]
            elif self.start[len(self.start) - 1][i] == '.':
                self.coordsExit += [[len(self.start) - 1, i]]
        for i in range(1, len(self.start) - 1):
            if self.start[i][0] == '.':
                self.coordsExit += [[i, 0]]
            elif self.start[i][len(self.start[0]) - 1] == '.':
                self.coordsExit += [[i, len(self.start[0]) - 1]]
        print(self.coordsExit)
        print("Stare Initiala:\n")
        pprint(self.start)

        # calcuez bounding box pt iesire
        self.exit_bbrow1 = float("inf")
        self.exit_bbcol1 = float("inf")
        self.exit_bbrow2 = 0
        self.exit_bbcol2 = 0

        for row, col in self.coordsExit:
            if row < self.exit_bbrow1:
                self.exit_bbrow1 = row
            if col < self.exit_bbcol1:
                self.exit_bbcol1 = col
            if row > self.exit_bbrow2:
                self.exit_bbrow2 = row
            if col > self.exit_bbcol2:
                self.exit_bbcol2 = col

    def testeaza_scop(self, nodCurent):
        return nodCurent.isScope()

    def genereazaSuccesori(self, nodCurent: NodParcurgere, tip_euristica="euristica banala"):
        """
            pentru fiecare piesa, creeaza cate un NodParcurgere pt fiecare directie in care se poate deplasa
            """
        dirs = ['n', 's', 'e', 'w']
        listaSucc = []
        for (name, piece) in nodCurent.info.items():
            for dir in dirs:
                if not nodCurent.canMovePiece(piece, dir):
                    continue
                new_board, new_info = nodCurent.movePiece(piece, dir)
                move_cost = piece.getCost()
                # stc atentie aici, posibil sa fie nevoie de info, nu de board
                if nodCurent.contineInDrum(new_board):
                    continue
                nod_nou = NodParcurgere(new_board, nodCurent, new_info, nodCurent.g + move_cost,
                                        self.calculeaza_h(nodCurent, tip_euristica), dir=dir, movedPiece=name, numar_ordine=self.noduri_generate)
                self.noduri_generate += 1
                listaSucc.append(nod_nou)
        return listaSucc

    def calculeaza_h(self, nod, tip_euristica="euristica banala"):
        if tip_euristica == "euristica banala":
            return 1

        elif tip_euristica == "euristica admisibila 1":
            return self.manhatan(nod)

        elif tip_euristica == "euristica admisibila 2":
            # verific daca exista cale libera pana la exit
            # daca da, returnez distanta manhattan
            # daca nu, ret distanta manhattan + costul celei mai ieftine piese intalnite
            met = {}
            viz = [[False for i in range(len(nod.board[0]))] for j in range(len(nod.board))]
            q = []
            d_row = [1, 0, -1, 0]
            d_col = [0, 1, 0, -1]
            for block in nod.info['*'].blocks:
                if not (0 <= block[0] < len(nod.board) and 0 <= block[1] < len(nod.board[1])):
                    continue
                q += ((block[0], block[1]),)
                viz[block[0]][block[1]] = True

            accesibile = 0
            found = False
            while len(q):
                block = q.pop(0)
                found = False
                for i in range(4):
                    neigh_row = block[0] + d_row[i]
                    neigh_col = block[1] + d_col[i]
                    if not (0 <= neigh_row < len(nod.board) and 0 <= neigh_col < len(nod.board[0])):
                        # AM GASIT EXIT
                        found = True
                        break
                    if not nod.board[neigh_row][neigh_col] in ['#', '.', '*']:
                        met[nod.board[neigh_row][neigh_col]] = True
                    if nod.board[neigh_row][neigh_col] != '.':
                        continue
                    accesibile += 1
                    if viz[neigh_row][neigh_col]:
                        continue
                    q += ((neigh_row, neigh_col),)
                    viz[neigh_row][neigh_col] = True

                if found:
                    break
            if found:
                return self.manhatan(nod)
            else:
                # returnez manhatan + costul de a muta cea mai ieftina intalnita\
                prices = [nod.info[name].getCost() for name in met.keys()]
                return self.manhatan(nod) + (min(prices) if len(prices) else 0)

        elif tip_euristica == "euristica neadmisibila 1":
            # adun catva la euristica pt fiecare pozitie in care nu se poate misca piesa speciala
            h = 0
            inc = 1
            dirs = ['s', 'n', 'e', 'w']
            for dir in dirs:
                if not nod.canMovePiece(nod.info['*'], dir):
                    h += inc
            return h

        elif tip_euristica == "euristica neadmisibila 2":
            # prioritizam mutarea piesei speciale
            return nod.info[nod.movedPiece].getCost() * 10 if nod.movedPiece not in [None, '*'] else 1


    def manhatan(self, nod):
        # manhatan distance
        piesa_speciala = nod.info['*']
        # # iau primul block din piesa speciala si consider pozitia lui, whatever
        # block = piesa_speciala.blocks[0]
        # # cost_pe_mutare = piesa_speciala.getCost()
        # spatii_de_parcurs = abs(block[0] - self.coordsExit[0][0]) + abs(block[1] - self.coordsExit[0][1])
        # manhatan_maxim = (len(nod.board)-2) + (len(nod.board[0])-2)
        # # return manhatan_maxim - spatii_de_parcurs
        # return spatii_de_parcurs

        deltaRow = deltaCol = 0
        startRow, startCol, finalRow, finalCol = piesa_speciala.getBB()

        if len(self.coordsExit) == 0:
            return 1
        if self.coordsExit[0][0] == 0:  # iesirea e sus
            deltaRow = finalRow
            deltaCol = min(abs(finalCol - self.exit_bbcol2), abs(startCol - self.exit_bbcol1))
        elif self.coordsExit[0][0] == len(nod.board) - 1:  # jos
            deltaRow = abs(len(nod.board) - startRow) - 1
            deltaCol = min(abs(finalCol - self.exit_bbcol2), abs(startCol - self.exit_bbcol1))
        elif self.coordsExit[0][1] == 0:  # stanga
            deltaRow = min(abs(finalRow - self.exit_bbrow2), abs(startRow - self.exit_bbrow1))
            deltaCol = finalCol
        elif self.coordsExit[0][1] == len(nod.board[0]) - 1:  # dreapta
            deltaRow = min(abs(finalRow - self.exit_bbrow2), abs(startRow - self.exit_bbrow1))
            deltaCol = abs(startCol - self.exit_bbcol1)
        return deltaRow + deltaCol

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)