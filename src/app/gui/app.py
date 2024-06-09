from kivy.app import App
from kivy.core.window import Window

from src.app.gui.menu_and_participants_list import MainScreen


class SumioApp(App):

    def build(self):
        Window.maximize()
        return MainScreen()
