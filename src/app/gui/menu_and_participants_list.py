import logging
from functools import partial
from tkinter import messagebox

import pandas as pd
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from src.app.backend.ParticipantsManager import ParticipantsManager
from src.app.config.constraints import CONSTRAINTS
from src.app.csv_reader import csv_reader
from src.app.gui.bracket import Bracket
from src.app.gui.quick_start import QuickStart
from src.app.gui.wrestler_profile import WrestlerSelectedStatus, WrestlerProfile


class MainScreen(BoxLayout):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.update_content('Quick Start')
        self.participants = ParticipantsManager()

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

            show_participants = ShowParticipants(self.init_dataframe(csv_reader.df), self.participants)
            content.add_widget(show_participants)
            # until we change the way we route screens,
            # the method "generate_layout" has to be invoked after "content.add_widget(show_participants)"
            show_participants.generate_layout()

        elif item == 'Bracket':
            if self.participants.length() < 2 or self.participants.length() > 16:
                messagebox.showerror("Error", "Invalid contestant number, must be between 2 and 16")
            else:
                content.add_widget(Bracket())

    def init_dataframe(self, df):
        df['age'] = df['date_of_birth'].apply(csv_reader.birthDateToAge)
        df = self.swap_df_columns(df, 3, 8)
        return df

    @staticmethod
    def swap_df_columns(df, idx1, idx2):
        cols = list(df)
        cols[idx2], cols[idx1] = cols[idx1], cols[idx2]
        return df.loc[:, cols]

    def update_content_and_show_wrestler(self, wrestler_data: pd.Series):
        content = self.ids.content
        content.clear_widgets()

        wrestler_status = WrestlerSelectedStatus(self.participants.is_selected(wrestler_data))
        wrestler_info = WrestlerProfile(wrestler_data, wrestler_status, self.participants)

        box_layout = BoxLayout(orientation='vertical', spacing=40)
        box_layout.add_widget(wrestler_info)
        box_layout.add_widget(wrestler_status)
        box_layout.add_widget(BoxLayout())

        content.add_widget(box_layout)


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


class LabelCheckBox(BoxLayout):
    def __init__(self, text='', bind=None, **kwargs):
        super(LabelCheckBox, self).__init__(**kwargs)
        self.orientation = 'horizontal'

        self.label = Label(text=text, color=(0.1294, 0.1294, 0.1294, 1))
        self.checkbox = CheckBox(
            color=(0.1294, 0.1294, 0.1294, 1),
            size_hint_x=None,
            width=10
        )
        if bind:
            self.checkbox.bind(active=bind)

        self.add_widget(self.checkbox)
        self.add_widget(self.label)


class ProfileButton(ButtonBehavior, Image):
    def __init__(self, wrestler: pd.Series, main_screen: MainScreen, **kwargs):
        super().__init__(**kwargs)
        self.wrestler = wrestler
        self.main_screen = main_screen

    def on_press(self):
        super().on_press()
        self.main_screen.update_content_and_show_wrestler(self.wrestler)


class ShowParticipants(ScrollView):

    def __init__(self, participants_data, participants_manager, **kwargs):
        super(ShowParticipants, self).__init__(**kwargs)
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
        self.participants_manager = participants_manager
        self.participants_data = participants_data
        self.filtered_data = participants_data
        self.visible_checkboxes = []
        self.headers = [header.replace('_', ' ').title() for header in CONSTRAINTS['required_columns'][:-1]]
        self.headers[3] = 'Age'
        self.headers.insert(0, "Profile")
        self.headers.append("Add to bracket")
        self.text_inputs = ['' for _ in range(len(self.headers) + 2)]
        self.init_filtering_keys()

    def init_filtering_keys(self):
        self.text_filter_keys = CONSTRAINTS['required_columns'][:-1]
        self.text_filter_keys.remove('date_of_birth')
        self.text_filter_keys.remove('weight')

    def generate_layout(self):

        layout = GridLayout(cols=9, spacing=26, size_hint_y=None, padding=[dp(20), dp(20)])
        layout.bind(minimum_height=layout.setter('height'))

        for header in self.headers:
            layout.add_widget(Label(text=header, bold=True, font_size=14, color=(0.1294, 0.1294, 0.1294, 1)))

        self.visible_checkboxes = []
        self.put_search_filters(layout)
        for _, participant in self.filtered_data.iterrows():
            self.add_participant_labels(layout, participant)

        self.add_widget(layout)

    def on_header_checkbox_click(self, checkbox, value):
        if value:
            for c in self.visible_checkboxes[:16]:
                c.active = True
        else:
            for c in self.visible_checkboxes:
                c.active = False

    def on_checkbox_click(self, participant, checkbox, value):
        if value:
            self.participants_manager.add(participant)
        else:
            self.participants_manager.remove(participant)

    def put_search_filters(self, layout):
        # empty widget to make place for the "profile" column
        layout.add_widget(Widget())
        layout.add_widget(
            TextInput(
                hint_text="Filter Name", text=self.text_inputs[0],
                on_text_validate=self.apply_filters, multiline=False
            )
        )
        layout.add_widget(
            TextInput(
                hint_text="Filter Surname", text=self.text_inputs[1],
                on_text_validate=self.apply_filters, multiline=False
            )
        )
        layout.add_widget(
            TextInput(
                hint_text="Filter Age Cat.", text=self.text_inputs[2],
                on_text_validate=self.apply_filters, multiline=False
            )
        )
        age_layout = GridLayout(cols=2, spacing=5)
        age_layout.add_widget(
            TextInput(
                hint_text="Min", text=str(self.text_inputs[3]),
                on_text_validate=self.apply_filters, multiline=False
            )
        )
        age_layout.add_widget(
            TextInput(
                hint_text="Max", text=str(self.text_inputs[4]),
                on_text_validate=self.apply_filters, multiline=False
            )
        )
        layout.add_widget(age_layout)
        layout.add_widget(
            TextInput(
                hint_text="Filter Weight Cat.", text=self.text_inputs[5],
                on_text_validate=self.apply_filters, multiline=False
            )
        )
        weight_layout = GridLayout(cols=2, spacing=5)
        weight_layout.add_widget(
            TextInput(
                hint_text="Min", text=str(self.text_inputs[6]),
                on_text_validate=self.apply_filters, multiline=False
            )
        )
        weight_layout.add_widget(
            TextInput(
                hint_text="Max", text=str(self.text_inputs[7]),
                on_text_validate=self.apply_filters, multiline=False
            )
        )
        layout.add_widget(weight_layout)
        layout.add_widget(
            TextInput(
                hint_text="Filter Country", text=self.text_inputs[8],
                on_text_validate=self.apply_filters, multiline=False
            )
        )
        layout.add_widget(
            LabelCheckBox(
                text="(max 16)",
                bind=self.on_header_checkbox_click
            )
        )

    def add_participant_labels(self, layout, participant):
        # add a button that takes the user to the wrestler's profile
        btn = ProfileButton(participant, self.parent.parent, source="./resources/icons/user_in_circle_48.png")
        anch = AnchorLayout(anchor_x='center', anchor_y='center')
        anch.add_widget(btn)
        layout.add_widget(anch)

        for label_name in self.filtered_data.columns[:-2]:
            layout.add_widget(
                Label(
                    text=str(participant[label_name]),
                    font_size=12,
                    color=(0.1294, 0.1294, 0.1294, 1)
                )
            )
        active = False
        if self.participants_manager.is_selected(participant):
            active = True

        checkbox = CheckBox(
            size_hint_y=None,
            height=dp(14),
            color=(0.1294, 0.1294, 0.1294, 1),
            active=active
        )
        self.visible_checkboxes.append(checkbox)
        check = partial(self.on_checkbox_click, participant)
        checkbox.bind(active=check)
        layout.add_widget(checkbox)

    def add_numeric_filter_range(self, key):
        input_range = [
            self.numeric_data_info[key]['constraints'][0],
            100000
        ]
        for i, val in enumerate(self.numeric_data_info[key]['column_indices']):
            data_val = self.text_inputs[val]
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
        self.text_inputs = self.get_filter_inputs()
        age_input_range = self.add_numeric_filter_range('age')
        weight_input_range = self.add_numeric_filter_range('weight')

        self.filtered_data = self.participants_data.loc[
            (self.participants_data['age'].between(*age_input_range)) &
            (self.participants_data['weight'].between(*weight_input_range))
            ]
        logging.info(f"Applied age filter: {age_input_range}")
        logging.info(f"Applied weight filter: {weight_input_range}")

        text_filters = [
            text.strip() for i, text in enumerate(self.text_inputs)
            if i not in self.numeric_data_info['age']['column_indices']
            and i not in self.numeric_data_info['weight']['column_indices']
        ]
        for i, text in enumerate(text_filters):
            if text:
                self.filtered_data = self.filtered_data.loc[
                    (self.participants_data[self.text_filter_keys[i]].str.lower().str.contains(text.lower()))
                ]
        logging.info(f"Applied text filters: {text_filters}")

        self.clear_widgets()
        self.generate_layout()
