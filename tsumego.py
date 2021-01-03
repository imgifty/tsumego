from board import Board, Stone


class Tsumego:
    def __init__(self, sgf):
        self.board = Board()

        game_tree = sgf.children[0]
        root = game_tree.nodes[0]

        self.init_state = root
        self.state = root
        self.init_stones(root)

    def init_stones(self, node):
        black = node.properties['AB']
        white = node.properties['AW']

        for stone in black:
            index = Tsumego.convert_sgf_position(stone)
            self.board.place_stone(index, Stone.BLACK)

        for stone in white:
            index = Tsumego.convert_sgf_position(stone)
            self.board.place_stone(index, Stone.WHITE)

    def reset(self):
        self.state = self.init_state
        self.board = Board()
        self.init_stones(self.init_state)

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