from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout


class SumioApp(App):
    kv_file = './kivy/app.kv'

    def build(self):
        return MainScreen()


class MainScreen(BoxLayout):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.update_content('Quick Start')

    def update_content(self, item):
        content = self.ids.content
        content.clear_widgets()
        if item == 'Quick Start':
            content.add_widget(QuickStart())
        elif item == 'Load CSV file':
            content.add_widget(LoadCSV())
        elif item == 'Show participants':
            content.add_widget(ShowParticipants())
        elif item == 'Bracket':
            content.add_widget(Bracket())


class Menu(BoxLayout):
    pass


class MenuItem(BoxLayout):
    text1 = StringProperty("")
    text2 = StringProperty("")

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.button == 'left':
                root = self.parent.parent
                root.update_content(self.text1)
                return True
        return super(MenuItem, self).on_touch_down(touch)


class Content(BoxLayout):
    pass


class QuickStart(BoxLayout):
    pass


class LoadCSV(BoxLayout):
    pass


class ShowParticipants(BoxLayout):
    pass


class Bracket(BoxLayout):
    pass


if __name__ == "__main__":
    SumioApp().run()
