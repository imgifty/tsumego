import kivy
from kivy.config import Config
kivy.require('2.0.0')

Config.set('graphics','resizable',0)
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '800')

from kivy.core.text import Label as CoreLabel
from kivy.core.text.markup import MarkupLabel as CoreMarkupLabel

from kivy.properties import NumericProperty
from kivy.app import App
from kivy.resources import resource_find
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.core.window import Window

from board import Board, Stone


class BadukPane(Widget):
    def update(self):
        self.canvas.clear()
        for i in range(len(self.controller.board)):
            row, col = Board.un_flatten(i)
            color = self.controller.board[i]
            if color == Stone.WHITE:
                self.draw_stone(1, row, col)
            elif color == Stone.BLACK:
                self.draw_stone(0, row, col)

    def register_controller(self, controller):
        self.controller = controller

    def compute_margins(self):
        self.margin = 50
        self.board_size = Window.height - 2*self.margin
        self.big_margin = (Window.width - self.board_size) // 2
        self.board_margin = 40
        self.game_pos_x = self.pos[0] + self.big_margin + self.board_margin + 1
        self.game_pos_y = self.pos[1] + self.margin + self.board_margin + 1
        self.game_size = self.board_size - 2*self.board_margin - 2
        self.line_margin = self.game_size / 18

    def on_touch_down(self, touch):
        if not hasattr(self, 'color'):
            self.color = True

        self.color = not self.color
        row, col = self.get_coordinate(touch.pos)
        if 0 <= row < 19 and 0 <= col < 19:
            out = self.controller.suggest_move((col, row))
            print(out)

            if out:
                more = self.controller.advance()
                print(more)
                if more:
                    self.controller.advance()

    def get_coordinate(self, position):
        col = round((position[0] - self.game_pos_x) / self.line_margin)
        row = round(18 - (position[1] - self.game_pos_y) / self.line_margin)

        return row, col

    def draw_coordinates(self):
        text_offset = 25

        with self.canvas.before:
            Color(0, 0, 0)
            for i in range(19):
                letter = chr(ord('A') + i)
                self.draw_text(pos=(self.game_pos_x + i * self.line_margin,
                                    self.game_pos_y + self.game_size + text_offset),
                                    text=letter, font_size=10, font_name="Roboto")
                self.draw_text(pos=(self.game_pos_x + i * self.line_margin,
                                    self.game_pos_y - text_offset),
                                    text=letter, font_size=10, font_name="Roboto")

                self.draw_text(pos=(self.game_pos_x - text_offset,
                                    self.game_pos_y + i * self.line_margin),
                                    text=str(i+1), font_size=10, font_name="Roboto")
                self.draw_text(pos=(self.game_pos_x + self.game_size + text_offset,
                                    self.game_pos_y + i * self.line_margin),
                                    text=str(i+1), font_size=10, font_name="Roboto")

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

        with self.canvas:
            Color(0, 0, 0)
            for column, row in points:
                Ellipse(pos=(self.game_pos_x + column * self.line_margin - stone_size/2,
                            self.game_pos_y + (18 - row) * self.line_margin - stone_size/2),
                            size=(stone_size, stone_size))

    def build_gui(self):
        self.compute_margins()
        self.draw_board()
        self.draw_coordinates()
        self.draw_star_points()

    def draw_stone(self, color, row, column):
        stone_size = 33, 33

        with self.canvas:
            if not color:
                Color(0, 0, 0)
            else:
                Color(1, 1, 1)
            Ellipse(pos=(self.game_pos_x + column * self.line_margin - stone_size[0]/2,
                         self.game_pos_y + (18 - row) * self.line_margin - stone_size[1]/2),
                         size=(stone_size[0], stone_size[1]))

    def draw_board(self):
        with self.canvas.before:
            Color(0.52, 0.37, 0.26)
            Rectangle(pos=(self.pos[0] + self.big_margin, self.pos[1] + self.margin),
                      size=(self.board_size, self.board_size))

            Color(0, 0, 0)
            Rectangle(pos=(self.pos[0] + self.big_margin + self.board_margin,
                           self.pos[1] + self.margin + self.board_margin),
                           size=(self.board_size - 2*self.board_margin, self.board_size - 2*self.board_margin))

            Color(0.52, 0.37, 0.26)
            Rectangle(pos=(self.game_pos_x,
                           self.game_pos_y),
                           size=(self.game_size, self.game_size))

            Color(0, 0, 0)
            for i in range(18):
                Line(points=[self.game_pos_x, self.game_pos_y + i * self.line_margin,
                             self.game_pos_x + self.game_size, self.game_pos_y + i * self.line_margin], width=1)
                Line(points=[self.game_pos_x + i * self.line_margin, self.game_pos_y,
                             self.game_pos_x + i * self.line_margin, self.game_pos_y + self.game_size], width=1)