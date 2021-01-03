import os

from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.config import Config
from kivy.clock import Clock
from kivy.properties import ObjectProperty

import sgf
from board import Tsumego

Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', '1400')
Config.set('graphics', 'height', '800')

from gui.baduk_pane import BadukPane # noqa
# from tracker import insert_problem, solved_daily_problem, get_solved_problems


def read_sgf(file_name):
    with open(file_name) as f:
        game = sgf.parse(f.read())
        return game


def get_random_game(seed):
    samples = '/home/alexander/Work/tsumego/samples/'
    book = ('CD 1 - FAMOUS TSUMEGO COMPOSERS/'
            'CHO CHIKUN Encyclopedia Life And Death - Elementary')
    collection = os.path.join(samples, book)

    files = [os.path.join(collection, f) for f in os.listdir(collection)]

    return read_sgf(files[seed])


class TsumegoWidget(BoxLayout):
    pane = ObjectProperty()
    next_button = ObjectProperty()
    current_seed = 0

    def init(self):
        Clock.schedule_once(lambda dt: self.pane.build_gui(), 0.1)
        Clock.schedule_once(lambda dt: self.init_tsumego(), 0.1)
        Clock.schedule_interval(lambda dt: self.update(), 0.1)

    def update(self):
        self.pane.update()

    def reset_tsumego(self):
        self.tsumego.reset()

    def init_tsumego(self):
        self.tsumego = Tsumego(get_random_game(self.current_seed))
        self.pane.register_controller(self.tsumego)
        self.update()
        self.current_seed += 1


class MainApp(App):
    def build(self):
        self.title = 'Baduk Trainer'
        self.widget = TsumegoWidget()
        self.widget.init()

        return self.widget

    def reset_game(self):
        self.widget.init_tsumego()


if __name__ == '__main__':
    MainApp().run()
