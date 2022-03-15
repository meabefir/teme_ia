class PieceMove:
    def __init__(self, board, piece, dir, duration):
        self.board = board
        self.piece = piece
        self.piece_name = piece.value
        self.dir = dir
        self.duration = duration
        self.frame = 0
        self.finished = False
        self.started = False

        self.distance_per_frame = board.cell_size / self.duration
        self.dx, self.dy = self.interpretDirection(dir)

    def start(self):
        self.started = True

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
        self.piece.translate(self.dx * self.distance_per_frame, self.dy * self.distance_per_frame)

        if self.frame >= self.duration:
            drow, dcol = self.interpretMatrixDirection(self.dir)
            self.piece.move(drow, dcol)
            self.finished = True