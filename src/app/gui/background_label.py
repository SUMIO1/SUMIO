from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label


class BackgroundLabel(Label):

    def __init__(self, key: str = "", bg_color: tuple[float, ...] = (0, 0, 0, 0), **kwargs):
        super(BackgroundLabel, self).__init__(**kwargs)
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.key = key

        with self.canvas.before:
            Color(rgba=bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_color(self, r, g, b, a):
        with self.canvas.before:
            Color(rgba=(r, g, b, a))
            self.rect = Rectangle(size=self.size, pos=self.pos)
