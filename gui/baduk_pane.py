import kivy
kivy.require('2.0.0')

from kivy.core.audio import SoundLoader
from kivy.core.text import Label as CoreLabel
from kivy.core.text.markup import MarkupLabel as CoreMarkupLabel
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)

from kivy.properties import NumericProperty
from kivy.app import App
from kivy.clock import Clock
from kivy.resources import resource_find
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.core.window import Window
from kivy.lang import Builder

from board import Board, Stone

Builder.load_file('gui/badukpane.kv')

class BadukPane(Widget):
    def __init__(self, **kwargs):
        super(BadukPane, self).__init__(**kwargs)
        self.bind(pos=self.update_rect,
                  size=self.update_rect)
        self.stone_sound = SoundLoader.load('sounds/stone3.wav')
        self.solved_sound = SoundLoader.load('sounds/bell.wav')
        self.solved_sound.volume = 0.2


    def update_rect(self, *args):
        self.canvas_pos = self.pos
        self.canvas_size = self.size

    def update(self):
        self.canvas.clear()
        self.build_gui()
        for i in range(len(self.controller.board.board)):
            row, col = Board.un_flatten(i)
            color = self.controller.board.board[i]
            if color == Stone.WHITE:
                self.draw_stone(1, row, col)
            elif color == Stone.BLACK:
                self.draw_stone(0, row, col)

    def register_controller(self, controller):
        self.controller = controller

    def compute_margins(self):
        self.margin = 50
        self.board_size = self.canvas_size[1] - 2 * self.margin
        self.big_margin = (self.canvas_size[0] - self.board_size) // 2
        self.board_margin = 40
        self.game_pos_x = self.canvas_pos[0] + self.big_margin + self.board_margin + 1
        self.game_pos_y = self.canvas_pos[1] + self.margin + self.board_margin + 1
        self.game_size = self.board_size - 2*self.board_margin - 2
        self.line_margin = self.game_size / 18

    def on_touch_down(self, touch):
        if not hasattr(self, 'color'):
            self.color = True

        self.color = not self.color
        row, col = self.get_coordinate(touch.pos)
        if 0 <= row < 19 and 0 <= col < 19:
            if self.controller.has_next():
                correct = self.controller.check_move((col, row))

                if correct:
                    self.stone_sound.play()
                    self.controller.advance()

                    if self.controller.has_next():
                        Clock.schedule_once(lambda dt: self.stone_sound.play(), 0.4)
                        Clock.schedule_once(lambda dt: self.controller.advance(), 0.4)
                    else:
                        self.solved_sound.play()

    def get_coordinate(self, position):
        col = round((position[0] - self.game_pos_x) / self.line_margin)
        row = round(18 - (position[1] - self.game_pos_y) / self.line_margin)

        return row, col

    def draw_coordinates(self):
        text_offset = 27
        font_size = 15

        with self.canvas.before:
            Color(0, 0, 0)
            for i in range(19):
                letter = chr(ord('A') + i)
                self.draw_text(pos=(self.game_pos_x + i * self.line_margin,
                                    self.game_pos_y + self.game_size + text_offset),
                                    text=letter, font_size=font_size, font_name="Roboto")
                self.draw_text(pos=(self.game_pos_x + i * self.line_margin,
                                    self.game_pos_y - text_offset),
                                    text=letter, font_size=font_size, font_name="Roboto")

                self.draw_text(pos=(self.game_pos_x - text_offset,
                                    self.game_pos_y + i * self.line_margin),
                                    text=str(i+1), font_size=font_size, font_name="Roboto")
                self.draw_text(pos=(self.game_pos_x + self.game_size + text_offset,
                                    self.game_pos_y + i * self.line_margin),
                                    text=str(i+1), font_size=font_size, font_name="Roboto")

    def draw_text(self, pos, text, font_name=None, markup=False, **kwargs):
        texture = self.cached_text_texture(text, font_name, markup, **kwargs)
        Rectangle(
            texture=texture, pos=(pos[0] - texture.size[0] / 2, pos[1] - texture.size[1] / 2), size=texture.size,
        )

    def cached_text_texture(self, text, font_name, markup, _cache={}, **kwargs):
        args = (text, font_name, markup, *[(k, v) for k, v in kwargs.items()])
        texture = _cache.get(args)
        if texture:
            return texture

        label_cls = CoreMarkupLabel if markup else CoreLabel
        label = label_cls(text=text, bold=True, font_name=font_name, **kwargs)
        label.refresh()
        texture = _cache[args] = label.texture

        return texture

    def draw_star_points(self):
        stone_size = 10
        points = [(3, 3), (9, 3), (9, 9), (15, 15), (15, 3), (15, 9), (3, 15), (9, 15), (3, 9)]

        with self.canvas.before:
            Color(0, 0, 0)
            for column, row in points:
                Ellipse(pos=(self.game_pos_x + column * self.line_margin - stone_size/2,
                            self.game_pos_y + (18 - row) * self.line_margin - stone_size/2),
                            size=(stone_size, stone_size))

    def build_gui(self):
        if hasattr(self, "canvas_pos") and hasattr(self, "canvas_size"):
            self.compute_margins()
            self.draw_board()
            self.draw_coordinates()
            self.draw_star_points()

    def draw_stone(self, color, row, column):
        stone_size = 32

        with self.canvas:
            if not color:
                Color(0, 0, 0)
            else:
                Color(1, 1, 1)
            Ellipse(pos=(self.game_pos_x + column * self.line_margin - stone_size/2,
                         self.game_pos_y + (18 - row) * self.line_margin - stone_size/2),
                         size=(stone_size, stone_size))

    def draw_board(self):
        with self.canvas.before:
            Color(0.52, 0.37, 0.26)
            Rectangle(pos=(self.canvas_pos[0] + self.big_margin + 1, self.canvas_pos[1] + self.margin),
                      size=(self.board_size, self.board_size))

            Color(0.52, 0.37, 0.26)
            Rectangle(pos=(self.game_pos_x,
                           self.game_pos_y),
                           size=(self.game_size, self.game_size))

            Color(0, 0, 0)
            for i in range(19):
                Line(points=[self.game_pos_x, self.game_pos_y + i * self.line_margin,
                             self.game_pos_x + self.game_size, self.game_pos_y + i * self.line_margin], width=1)
                Line(points=[self.game_pos_x + i * self.line_margin, self.game_pos_y,
                             self.game_pos_x + i * self.line_margin, self.game_pos_y + self.game_size], width=1)