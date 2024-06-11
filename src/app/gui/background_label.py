from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label


class BackgroundLabel(Label):
    def __init__(self, bg_color: tuple[float, ...] = (0, 0, 0, 0), **kwargs):
        super(BackgroundLabel, self).__init__(**kwargs)
        self.bind(pos=self.update_rect, size=self.update_rect)

        with self.canvas.before:
            Color(rgba=bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
