import random
import os
import sgf

from kivy.app import App
from kivy.clock import Clock
from gui.baduk_pane import BadukPane
from board import Board, Stone
from tracker import insert_problem, solved_daily_problem, get_solved_problems


def read_sgf(file_name):
    with open(file_name) as f:
        game = sgf.parse(f.read())
        return game


class MainApp(App):
    def build(self):
        self.title = 'Baduk Trainer'
        self.pane = BadukPane()
        self.pane.build_gui()

        Clock.schedule_interval(lambda dt: self.update(), 1)

        samples = '/home/alexander/Work/tsumego/samples/'
        collection = os.path.join(samples, 'CD 1 - FAMOUS TSUMEGO COMPOSERS/CHO CHIKUN Encyclopedia Life And Death - Elementary')

        files = [os.path.join(collection, f) for f in os.listdir(collection)]
        seed = random.choice(range(len(files)))

        game = read_sgf(files[seed])
        assert len(game.children) == 1
        game_tree = game.children[0]
        nodes = game_tree.nodes
        node = nodes[0]

        self.board = Board(node)
        self.pane.register_controller(self.board)
        self.update()

        return self.pane

    def update(self):
        self.pane.update()


if __name__ == '__main__':
    MainApp().run()
