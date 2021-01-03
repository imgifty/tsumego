import random
import os

from kivy.uix.label import Label
from kivy.app import App
from kivy.clock import Clock

import sgf
from gui.baduk_pane import BadukPane
from board import Board, Stone, Tsumego
from tracker import insert_problem, solved_daily_problem, get_solved_problems


def read_sgf(file_name):
    with open(file_name) as f:
        game = sgf.parse(f.read())
        return game


def get_random_game(seed):
    samples = '/home/alexander/Work/tsumego/samples/'
    collection = os.path.join(samples, 'CD 1 - FAMOUS TSUMEGO COMPOSERS/CHO CHIKUN Encyclopedia Life And Death - Elementary')

    files = [os.path.join(collection, f) for f in os.listdir(collection)]

    return read_sgf(files[seed])


class MainApp(App):
    def build(self):
        self.title = 'Baduk Trainer'
        self.pane = BadukPane()
        self.pane.build_gui()

        Clock.schedule_interval(lambda dt: self.update(), 0.1)
        self.current_seed = 1

        self.reset_game()
        self.update()

        return self.pane

    def update(self):
        self.pane.update()

    def reset_game(self):
        self.current_seed += 1
        self.tsumego = Tsumego(get_random_game(self.current_seed))

        if self.tsumego.get_starting_player() == Stone.BLACK:
            Label(text="Black")
            print('BLACK')

        self.pane.register_controller(self.tsumego)
        self.update()


if __name__ == '__main__':
    MainApp().run()
