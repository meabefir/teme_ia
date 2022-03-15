import copy

class Piece:
    def __init__(self, board, value):
        self.board = board
        self.value = value
        self.blocks = []

    def splitsIfRemove(self, row, col):
        if len(self.blocks) == 1:
            return False

        cpy = copy.deepcopy(self.blocks)
        cpy.remove([row, col])

        drow = [1,0,-1,0]
        dcol = [0,1,0,-1]
        visited = []
        q = [cpy[0]]
        # daca le intalnim pe toate in parcurgere inseamna ca nu le desparte
        met = 0
        while len(q):
            current = q.pop(0)
            if current in visited:
                continue
            if not current in cpy:
                continue
            visited += [current]
            met += 1
            for i in range(4):
                next_row = current[0] + drow[i]
                next_col = current[1] + dcol[i]
                q += [[next_row, next_col]]

        return met != len(self.blocks) - 1

    def addBlock(self, row, col):
        self.blocks += [[row, col]]

    def removeBlock(self, row, col):
        self.blocks.remove([row, col])
        if len(self.blocks) == 0:
            self.board.removePiece(self.value)

    def neighOf(self, row, col):
        dirs = [[row+1, col], [row-1, col], [row, col+1], [row, col-1]]
        for block in self.blocks:
            for dir in dirs:
                if block == dir:
                    return True
        return False

    def move(self, dx, dy):
        for block in self.blocks:
            # cell = self.board.data[block[0]][block[1]]
            # cell.move(dx, dy)
            self.board.data[block[0]][block[1]].move(dx, dy)

    def __str__(self):
        ret = ""
        ret += str(self.value) + '\n'
        for block in self.blocks:
            ret += str(block) + ", "
        ret += '\n'
        return ret

    def __repr__(self):
        return str(self)