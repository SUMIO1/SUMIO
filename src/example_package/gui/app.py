from kivy.app import App
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

import pandas as pd


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


# name,surname,age_category,age,weight_category,weight,country,image_url

class ShowParticipants(ScrollView):

    def __init__(self, **kwargs):
        super(ShowParticipants, self).__init__(**kwargs)
        self.participants_data = pd.read_csv('sample.csv')

        # layout = GridLayout(cols=8, spacing=26, size_hint_y=None, padding=[dp(20), dp(20)])
        layout = GridLayout(cols=7, spacing=26, size_hint_y=None, padding=[dp(20), dp(20)])
        layout.bind(minimum_height=layout.setter('height'))

        # headers = ['Name', 'Surname', 'Age Category', 'Age', 'Weight Category', 'Weight', 'Country', '']
        headers = ['Name', 'Surname', 'Age Category', 'Age', 'Weight Category', 'Weight', 'Country']
        for header in headers:
            layout.add_widget(Label(text=header, bold=True, font_size=14))

        for index, participant in self.participants_data.iterrows():
            layout.add_widget(Label(text=str(participant['name']), font_size=12))
            layout.add_widget(Label(text=str(participant['surname']), font_size=12))
            layout.add_widget(Label(text=str(participant['age_category']), font_size=12))
            layout.add_widget(Label(text=str(participant['age']), font_size=12))
            layout.add_widget(Label(text=str(participant['weight_category']), font_size=12))
            layout.add_widget(Label(text=str(participant['weight']), font_size=12))
            layout.add_widget(Label(text=str(participant['country']), font_size=12))

            # add_button = Button(text="Add", size_hint=(None, None), size=(dp(40), dp(20)))
            # add_button.bind(on_release=self.print_participant)
            # layout.add_widget(add_button)

        self.add_widget(layout)

    def print_participant(self, instance):
        index = instance.parent.children.index(instance)
        participant = self.participants_data.iloc[index // 8]
        print(participant)


class Bracket(BoxLayout):
    pass


if __name__ == "__main__":
    SumioApp().run()
