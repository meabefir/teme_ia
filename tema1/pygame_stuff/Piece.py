import copy


class Piece:
    def __init__(self, board, value):
        self.board = board
        self.value = value
        self.blocks = []

    def canMoveTo(self, dir):
        drow, dcol = 0, 0
        if dir == 'n':
            drow, dcol = -1, 0
        elif dir == 's':
            drow, dcol = 1, 0
        elif dir == 'w':
            drow, dcol = 0, -1
        else:
            drow, dcol = 0, 1

        for block in self.blocks:
            n_row, n_col = block[0] + drow, block[1] + dcol
            if (0 <= n_row < len(self.board.data) and 0 <= n_col < len(self.board.data[0])):
                if self.board.data[n_row][n_col].value not in ['.', self.value]:
                    return False
        return True

    def splitsIfRemove(self, row, col):
        if len(self.blocks) == 1:
            return False

        cpy = copy.deepcopy(self.blocks)
        cpy.remove([row, col])

        drow = [1, 0, -1, 0]
        dcol = [0, 1, 0, -1]
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
        dirs = [[row + 1, col], [row - 1, col], [row, col + 1], [row, col - 1]]
        for block in self.blocks:
            for dir in dirs:
                if block == dir:
                    return True
        return False

    def translate(self, dx, dy):
        for block in self.blocks:
            if not self.board.inBounds(block[0], block[1]):
                continue
            cell = self.board.data[block[0]][block[1]]
            cell.translate(dx, dy)
            # self.board.data[block[0]][block[1]].translate(dx, dy)

    def move(self, drow, dcol):
        # update the board.data (the actual board matrix with cells)
        # update the blocks positions in the piece
        for block in self.blocks:
            if not self.board.inBounds(block[0], block[1]):
                continue
            self.board.data[block[0]][block[1]].assignValue('.')
            self.board.data[block[0]][block[1]].resetAfterTranslate()
        for block in self.blocks:
            if not self.board.inBounds(block[0], block[1]):
                continue
            block[0] += drow
            block[1] += dcol
        for block in self.blocks:
            if not self.board.inBounds(block[0], block[1]):
                continue
            self.board.data[block[0]][block[1]].assignValue(self.value)

        to_remove = []
        for block in reversed(self.blocks):
            if not self.board.inBounds(block[0], block[1]):
                to_remove += [block]
        for block in to_remove:
            self.removeBlock(block[0], block[1])

    def __str__(self):
        ret = ""
        ret += str(self.value) + '\n'
        for block in self.blocks:
            ret += str(block) + ", "
        ret += '\n'
        return ret

    def __repr__(self):
        return str(self)
