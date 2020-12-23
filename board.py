class Stone:
    BLACK = '⚫️'
    WHITE = '⚪️'
    NONE = '➕'


class Board:
    def __init__(self, node):
        self.board = [Stone.NONE for i in range(19*19)]
        self.init_state = node
        self.state = node
        self.init_stones(node)
    
    def init_stones(self, node):
        black = node.properties['AB']
        white = node.properties['AW']

        for stone in black:
            index = Board.convert_sgf_position(stone)
            self.board[index] = Stone.BLACK

        for stone in white:
            index = Board.convert_sgf_position(stone)
            self.board[index] = Stone.WHITE
    
    @staticmethod
    def convert_sgf_position(stone):
        index = Board.flatten(ord(stone[1]) - 97, ord(stone[0]) - 97)
        return index
    
    # TODO: add capture check!
    def advance(self):
        if self.state.next is not None:
            self.state = self.state.next
            added = self.state.properties
            color = 'B' if 'B' in added else 'W'
            value = added[color]
            assert len(value) == 1
            index = Board.convert_sgf_position(value[0])
            self.board[index] = Stone.WHITE if color == 'W' else Stone.BLACK
            return True
        return False
    
    def suggest_move(self, stone):
        next_state = self.state.next
        added = self.state.next.properties
        color = 'B' if 'B' in added else 'W'
        value = added[color]
        assert len(value) == 1

        should_be = Board.convert_sgf_position(value[0])
        move = Board.flatten(*stone)
        if should_be == move:
            return True
        return False

    def get_starting_player(self):
        next_state = self.init_state.next
        added = next_state.properties
        color = 'Black' if 'B' in added else 'White'
        return color
    
    def create_ascii_art(self):
        lines = []
        emojis = [f"{(num + 1) % 10}\N{COMBINING ENCLOSING KEYCAP}" for num in range(0, 19)]
        lines.append('  ' + ' '.join(emojis))
        for i in range(19):
            line = emojis[i] + ''.join(self.board[i*19:(i+1)*19])
            lines.append(line)
        return '\n'.join(lines)
    
    def reaches(self, index, color):
        visited = {}
        def search(current):
            neighbors = []
            pass
        
    
    @staticmethod
    def flatten(row, column):
        return column + 19 * row

    @staticmethod
    def un_flatten(index):
        column = index // 19
        row = index - (column * 19)
        return row, column