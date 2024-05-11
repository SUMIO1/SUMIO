from kivy.app import App
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from tkinter import messagebox
from example_package.csv_reader import csv_reader
from config.constraints import CONSTRAINTS

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


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


class ShowParticipants(ScrollView):

    def __init__(self, participants_data, **kwargs):
        super(ShowParticipants, self).__init__(**kwargs)
        self.participants_data = participants_data
        self.filtered_data = participants_data
        self.age_filter_range = (0, 100)
        self.weight_filter_range = (0, 200)
        self.generate_layout()

    def generate_layout(self):
        layout = GridLayout(cols=7, spacing=26, size_hint_y=None, padding=[dp(20), dp(20)])
        layout.bind(minimum_height=layout.setter('height'))
        self.text_filter_keys = CONSTRAINTS["required_columns"][:-1]
        self.headers = [header.replace('_', ' ').title() for header in self.text_filter_keys]

        self.put_search_button(layout)
        for header in self.headers:
            layout.add_widget(Label(text=header, bold=True, font_size=14, color=(0.1294, 0.1294, 0.1294, 1)))

        self.put_search_filters(layout)
        for index, participant in self.filtered_data.iterrows():
            self.add_participant_labels(layout, participant)

        self.add_widget(layout)

    def put_search_button(self, layout):
        n_grid = len(self.headers)
        for i in range(n_grid-1):
            if i == n_grid // 2:
                layout.add_widget(Button(text="Search", on_release=self.apply_filters))
            layout.add_widget(Label())

    def put_search_filters(self, layout):
        layout.add_widget(TextInput(hint_text="Filter Name", on_text_validate=self.apply_filters))
        layout.add_widget(TextInput(hint_text="Filter Surname", on_text_validate=self.apply_filters))
        layout.add_widget(TextInput(hint_text="Filter Age Category", on_text_validate=self.apply_filters))
        layout.add_widget(Slider(min=0, max=100, value=self.age_filter_range[1], on_value=self.apply_filters))
        layout.add_widget(TextInput(hint_text="Filter Weight Category", on_text_validate=self.apply_filters))
        layout.add_widget(Slider(min=0, max=200, value=self.weight_filter_range[1], on_value=self.apply_filters))
        layout.add_widget(TextInput(hint_text="Filter Country", on_text_validate=self.apply_filters))

    def add_participant_labels(self, layout, participant):
        for label_name in self.filtered_data.columns[:-1]:
            layout.add_widget(Label(text=str(participant[label_name]), font_size=12, color=(0.1294, 0.1294, 0.1294, 1)))

    def print_participant(self, instance):
        index = instance.parent.children.index(instance)
        participant = self.filtered_data.iloc[index // 8]
        print(participant)

    def apply_filters(self, *args):
        text_inputs = []
        sliders = []
        for child in self.children:
            if isinstance(child, GridLayout):
                for widget in child.children:
                    if isinstance(widget, TextInput):
                        text_inputs.append(widget.text)
                    elif isinstance(widget, Slider):
                        sliders.append(widget.value)
        
        text_inputs = text_inputs[::-1]
        # logging.debug(f"sasasa {text_inputs}")
        # logging.debug(f"sasasa sliders {sliders}")

        weight_filter = int(sliders[0])
        age_filter = int(sliders[1])
        self.filtered_data = self.participants_data.loc[
            (self.participants_data['age'].between(0, age_filter)) &
            (self.participants_data['weight'].between(0, weight_filter))
        ]

        text_filters = [text.strip() for text in text_inputs]
        # logging.debug(f"sasasa text filters {text_filters}")
        for i, text in enumerate(text_filters):
            if text:
                self.filtered_data = self.filtered_data.loc[
                    (self.participants_data[self.text_filter_keys[i]].str.lower() == text.lower())
                ]

        # logging.debug(f"Filtered data age {self.filtered_data['age']}")

        self.clear_widgets()
        self.generate_layout()


class Bracket(BoxLayout):
    pass


if __name__ == "__main__":
    SumioApp().run()
