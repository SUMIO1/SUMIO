from kivy.app import App
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from tkinter import messagebox
from src.example_package.csv_reader import csv_reader
from src.config.constraints import CONSTRAINTS


class SumioApp(App):
    kv_file = 'kivy/app.kv'

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
            csv_reader.readCSV()
        elif item == 'Show participants':
            if csv_reader.df is None:
                messagebox.showerror("Error", "No data to show. Please load a CSV file.")
                return
            content.add_widget(ShowParticipants(csv_reader.df))
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

    def __init__(self, participants_data, **kwargs):
        super(ShowParticipants, self).__init__(**kwargs)
        self.participants_data = participants_data
        self.generate_layout()

    def generate_layout(self):

        layout = GridLayout(cols=7, spacing=26, size_hint_y=None, padding=[dp(20), dp(20)])
        layout.bind(minimum_height=layout.setter('height'))

        headers = [header.replace('_', ' ').title() for header in CONSTRAINTS["required_columns"][:-1]]

        for header in headers:
            layout.add_widget(Label(text=header, bold=True, font_size=14, color=(0.1294, 0.1294, 0.1294, 1)))

        for index, participant in self.participants_data.iterrows():
            self.add_participant_labels(layout, participant)

        self.add_widget(layout)

    def add_participant_labels(self, layout, participant):
        for label_name in self.participants_data.columns[:-1]:
            layout.add_widget(Label(text=str(participant[label_name]), font_size=12, color=(0.1294, 0.1294, 0.1294, 1)))

    def print_participant(self, instance):
        index = instance.parent.children.index(instance)
        participant = self.participants_data.iloc[index // 8]
        print(participant)


class Bracket(BoxLayout):
    pass


if __name__ == "__main__":
    SumioApp().run()
