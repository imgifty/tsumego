class Stone:
    BLACK = 0
    WHITE = 1
    NONE = 2


class Board:
    def __init__(self):
        self.board = [Stone.NONE for i in range(19*19)]
        self.create_neighbours_lookup()

    def reaches(self, index, color):
        init_color = self.board[index]

        def dfs(index, color):
            states = [index]
            visited = set()

            while len(states) != 0:
                state = states.pop()

                if self.board[state] == color:
                    return True

                if state in visited:
                    continue
                visited.add(state)

                neighbours = [n for n in self.neighbours[state]
                              if (self.board[n] == init_color or
                              self.board[n] == color) and
                              n not in visited]
                states.extend(neighbours)

            return False

        return dfs(index, color)

    def create_neighbours_lookup(self):
        self.neighbours = {}

        for i in range(19*19):
            row, col = Board.un_flatten(i)
            others = [(row - i, col - j)
                      for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
            valid = [Board.flatten(*i)
                     for i in others if 0 <= i[0] < 19 and 0 <= i[1] < 19]
            self.neighbours[Board.flatten(row, col)] = valid

    def is_legal_move(self, index, color):
        ...

    def clear_color(self, color):
        new = self.board.copy()
        for i in range(19*19):
            if self.board[i] == color and not self.reaches(i, Stone.NONE):
                new[i] = Stone.NONE
        self.board = new

    def place_stone(self, index, color):
        self.board[index] = color
        other_color = Stone.WHITE if color == Stone.BLACK else Stone.BLACK
        self.clear_color(other_color)
        self.clear_color(color)

    @staticmethod
    def flatten(row, column):
        return column + 19 * row

    @staticmethod
    def un_flatten(index):
        column = index // 19
        row = index - (column * 19)
        return row, column