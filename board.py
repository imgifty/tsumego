class Stone:
    BLACK = '⚫️'
    WHITE = '⚪️'
    NONE = '➕'


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
                              if (self.board[n] == init_color or self.board[n] == color) and n not in visited]
                states.extend(neighbours)

            return False

        return dfs(index, color)

    def create_neighbours_lookup(self):
        self.neighbours = {}

        for i in range(19*19):
            row, col = Board.un_flatten(i)
            others = [(row - i, col - j) for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
            valid = [Board.flatten(*i) for i in others if 0 <= i[0] < 19 and 0 <= i[1] < 19]
            self.neighbours[Board.flatten(row, col)] = valid

    def is_legal_move(self, index, color):
        ...

    def clear_color(self, color):
        new = self.board.copy()
        for i in range(19*19):
            if self.board[i] == color and not self.reaches(i, Stone.NONE):
                print(Board.un_flatten(i))
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


class Tsumego:
    def __init__(self, sgf):
        self.board = Board()

        game_tree = sgf.children[0]
        root = game_tree.nodes[0]

        self.init_state = root
        self.state = root
        self.init_stones(root)

        a = self.board.reaches(Board.flatten(0, 0), Stone.WHITE)
        print(a)

    def init_stones(self, node):
        black = node.properties['AB']
        white = node.properties['AW']

        for stone in black:
            index = Tsumego.convert_sgf_position(stone)
            self.board.place_stone(index, Stone.BLACK)

        for stone in white:
            index = Tsumego.convert_sgf_position(stone)
            self.board.place_stone(index, Stone.WHITE)

    @staticmethod
    def convert_sgf_position(stone):
        index = Board.flatten(ord(stone[1]) - 97, ord(stone[0]) - 97)
        return index

    def has_next(self):
        if self.state.next is not None:
            return True
        return False

    def advance(self):
        if self.state.next is not None:
            self.state = self.state.next
            added = self.state.properties
            color = 'B' if 'B' in added else 'W'
            value = added[color]
            assert len(value) == 1
            index = Tsumego.convert_sgf_position(value[0])
            color = Stone.WHITE if color == 'W' else Stone.BLACK
            self.board.place_stone(index, color)
            return True
        return False

    def check_move(self, stone):
        next_state = self.state.next
        added = self.state.next.properties
        color = 'B' if 'B' in added else 'W'
        value = added[color]
        assert len(value) == 1

        should_be = Tsumego.convert_sgf_position(value[0])
        move = Board.flatten(*stone)
        if should_be == move:
            return True
        return False

    def get_starting_player(self):
        next_state = self.init_state.next
        added = next_state.properties
        color = Stone.BLACK if 'B' in added else Stone.WHITE
        return color