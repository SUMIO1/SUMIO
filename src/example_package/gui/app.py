from kivy.app import App
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from tkinter import messagebox
from src.example_package.csv_reader import csv_reader
from src.config.constraints import CONSTRAINTS

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class SumioApp(App):
    kv_file = 'kivy/app.kv'

    def build(self):
        Window.maximize()
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
        self.numeric_data_info = {
            'age': {
                'constraints': (0, CONSTRAINTS['age_categories']['Men']['max_age']),
                'column_indices': [3, 4]
            },
            'weight': {
                'constraints': (0, CONSTRAINTS['age_categories']['Men']['Heavy-weight']['max']),
                'column_indices': [6, 7]
            }
        }

        self.headers = [header.replace('_', ' ').title() for header in CONSTRAINTS['required_columns'][:-1]]
        self.init_filtering_keys()
        self.generate_layout()

    def init_filtering_keys(self):
        self.text_filter_keys = CONSTRAINTS['required_columns'][:-1]
        self.text_filter_keys.remove('age')
        self.text_filter_keys.remove('weight')

    def generate_layout(self):
        layout = GridLayout(cols=7, spacing=26, size_hint_y=None, padding=[dp(20), dp(20)])
        layout.bind(minimum_height=layout.setter('height'))
        self.put_search_button(layout)
        for header in self.headers:
            layout.add_widget(Label(text=header, bold=True, font_size=14, color=(0.1294, 0.1294, 0.1294, 1)))

        self.put_search_filters(layout)
        for _, participant in self.filtered_data.iterrows():
            self.add_participant_labels(layout, participant)

        self.add_widget(layout)

    def put_search_button(self, layout):
        n_grid = len(self.headers)
        for i in range(n_grid-1):
            if i == n_grid // 2:
                layout.add_widget(Button(text="Search", on_release=self.apply_filters))
            layout.add_widget(Label())

    def put_search_filters(self, layout):
        layout.add_widget(TextInput(hint_text="Filter Name", on_text_validate=self.apply_filters, multiline=False))
        layout.add_widget(TextInput(hint_text="Filter Surname", on_text_validate=self.apply_filters, multiline=False))
        layout.add_widget(TextInput(hint_text="Filter Age Cat.", on_text_validate=self.apply_filters, multiline=False))
        age_layout = GridLayout(cols=2, spacing=5)
        age_layout.add_widget(TextInput(hint_text="Min", on_text_validate=self.apply_filters, multiline=False))
        age_layout.add_widget(TextInput(hint_text="Max", on_text_validate=self.apply_filters, multiline=False))
        layout.add_widget(age_layout)
        layout.add_widget(TextInput(hint_text="Filter Weight Cat.", on_text_validate=self.apply_filters, multiline=False))
        weight_layout = GridLayout(cols=2, spacing=5)
        weight_layout.add_widget(TextInput(hint_text="Min", on_text_validate=self.apply_filters, multiline=False))
        weight_layout.add_widget(TextInput(hint_text="Max", on_text_validate=self.apply_filters, multiline=False))
        layout.add_widget(weight_layout)
        layout.add_widget(TextInput(hint_text="Filter Country", on_text_validate=self.apply_filters, multiline=False))

    def add_participant_labels(self, layout, participant):
        for label_name in self.filtered_data.columns[:-1]:
            layout.add_widget(Label(text=str(participant[label_name]), font_size=12, color=(0.1294, 0.1294, 0.1294, 1)))

    def add_numeric_filter_range(self, text_inputs, key):
        input_range = [
            self.numeric_data_info[key]['constraints'][0],
            self.numeric_data_info[key]['constraints'][1]
        ]
        for i, val in enumerate(self.numeric_data_info[key]['column_indices']):
            data_val = text_inputs[val]
            if not data_val or not data_val.isnumeric():
                continue
            data_val = int(data_val)
            if data_val in range(*input_range):
                input_range[i] = data_val

        return input_range

    def get_filter_inputs(self):
        text_inputs = []
        for child in self.children:
            if not isinstance(child, GridLayout):
                continue
            for widget in child.children:
                if isinstance(widget, TextInput):
                    text_inputs.append(widget.text)
                elif isinstance(widget, GridLayout):
                    for sub_widget in widget.children:
                        if not isinstance(sub_widget, TextInput):
                            continue
                        text_inputs.append(sub_widget.text)
        return text_inputs[::-1]

    def apply_filters(self, *args):
        text_inputs = self.get_filter_inputs()
        age_input_range = self.add_numeric_filter_range(text_inputs, 'age')
        weight_input_range = self.add_numeric_filter_range(text_inputs, 'weight')
        logging.info(f"Applied age filter: {age_input_range}")
        logging.info(f"Applied weight filter: {weight_input_range}")

        self.filtered_data = self.participants_data.loc[
            (self.participants_data['age'].between(*age_input_range)) &
            (self.participants_data['weight'].between(*weight_input_range))
        ]

        text_filters = [
            text.strip() for i, text in enumerate(text_inputs) \
            if i not in self.numeric_data_info['age']['column_indices'] \
            and i not in self.numeric_data_info['weight']['column_indices']
        ]
        logging.info(f"Applied text filters: {text_filters}")
        for i, text in enumerate(text_filters):
            if text:
                self.filtered_data = self.filtered_data.loc[
                    (self.participants_data[self.text_filter_keys[i]].str.lower() == text.lower())
                ]

        self.clear_widgets()
        self.generate_layout()


class Bracket(BoxLayout):
    pass


if __name__ == "__main__":
    SumioApp().run()
