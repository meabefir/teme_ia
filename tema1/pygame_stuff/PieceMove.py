class PieceMove:
    def __init__(self, board, piece_name, dir, duration):
        self.board = board
        self.piece_name = piece_name
        self.dir = dir
        self.duration = duration
        self.frame = 0
        self.finished = False

        self.distance_per_frame = board.cell_size / self.duration
        self.dx, self.dy = self.interpretDirection(dir)

    def interpretDirection(self, dir):
        if dir == 'n':
            return 0, -1
        elif dir == 's':
            return 0, 1
        elif dir == 'w':
            return -1, 0
        else:
            return 1, 0

    def interpretMatrixDirection(self, dir):
        if dir == 'n':
            return -1, 0
        elif dir == 's':
            return 1, 0
        elif dir == 'w':
            return 0, -1
        else:
            return 0, 1

    def update(self):
        if self.finished == True:
            return
        self.frame += 1
        self.board.pieces[self.piece_name].move(self.dx * self.distance_per_frame, self.dy * self.distance_per_frame)

        if self.frame >= self.duration:
            # TODO
            # update the blocks positions in the piece
            # update the board.data (the actual board matrix with cells)
            self.finished = True