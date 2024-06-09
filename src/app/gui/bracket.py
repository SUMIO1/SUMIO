from collections import defaultdict

from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.graphics import Color, Rectangle

import pandas as pd
import numpy as np


class TabbedCompetition(TabbedPanel):
    def __init__(self, participants_dataframe: pd.DataFrame, labels: defaultdict, **kwargs):
        super(TabbedCompetition, self).__init__(**kwargs)

        self.labels = labels

        self.regular_bracket_tab = TabbedPanelItem(text='Bracket')
        self.regular_bracket_tab.add_widget(CompetitionBracket(participants_dataframe=participants_dataframe,
                                                               labels=self.labels))
        self.add_widget(self.regular_bracket_tab)

        self.repechage_bracket_tab = TabbedPanelItem(text='Repechage')
        self.repechage_bracket_tab.add_widget(CompetitionBracket(participants_dataframe=participants_dataframe,
                                                                 labels=self.labels,
                                                                 repechage=True))
        self.add_widget(self.repechage_bracket_tab)


class CompetitionBracket(FloatLayout):
    def __init__(self, participants_dataframe: pd.DataFrame, labels: defaultdict, repechage: bool = False, **kwargs):
        super(CompetitionBracket, self).__init__(**kwargs)
        competitors_no = len(participants_dataframe)

        self.participants_dataframe = participants_dataframe
        self.repechage = repechage
        self.labels = labels

        if self.repechage:
            if competitors_no == 2:
                background = './resources/images/placeholder.png'
            elif 3 <= competitors_no <= 4:
                background = './resources/images/placeholder.png'
            elif 5 <= competitors_no <= 8:
                background = './resources/images/background_5_8_re.png'
            elif 9 <= competitors_no <= 16:
                background = './resources/images/placeholder.png'
            else:
                background = './resources/images/placeholder.png'
        else:
            if competitors_no == 2:
                background = './resources/images/placeholder.png'
            elif 3 <= competitors_no <= 4:
                background = './resources/images/placeholder.png'
            elif 5 <= competitors_no <= 8:
                background = './resources/images/background_5_8.png'
            elif 9 <= competitors_no <= 16:
                background = './resources/images/placeholder.png'
            else:
                background = './resources/images/placeholder.png'

        self.positions = defaultdict(dict)

        self.positions.update({
            "b1_1_1": {'x': -380, 'y': 195},
            "b1_1_2": {'x': -380, 'y': 140},
            "b1_2_1": {'x': -380, 'y': -192},
            "b1_2_2": {'x': -380, 'y': -246},
            "b1_3_1": {'x': 213, 'y': 195},
            "b1_3_2": {'x': 213, 'y': 140},
            "b1_4_1": {'x': 213, 'y': -192},
            "b1_4_2": {'x': 213, 'y': -246},
            "b2_1_1": {'x': -280, 'y': -1},
            "b2_1_2": {'x': -280, 'y': -55},
            "b2_2_1": {'x': 123, 'y': -1},
            "b2_2_2": {'x': 123, 'y': -5},
            "b3_1_1": {'x': -78, 'y': -1},
            "b3_1_2": {'x': -78, 'y': -55}
        })

        self.positions.update({
            "r1_1_1": {'x': -304, 'y': 295},
            "r1_1_2": {'x': -304, 'y': 240},
            "r1_2_1": {'x': -304, 'y': -275},
            "r1_2_2": {'x': -304, 'y': -332},
            "r2_1_1": {'x': -103, 'y': 97},
            "r2_1_2": {'x': -103, 'y': 42},
            "r2_2_1": {'x': -103, 'y': -77},
            "r2_2_2": {'x': -103, 'y': -135},
            "r3_1_1": {'x': 168, 'y': 15},
            "r3_1_2": {'x': 168, 'y': -41}
        })

        self.background_image = Image(source=background, allow_stretch=False, keep_ratio=True,
                                      pos_hint={'x': 0, 'y': 0}, size=(800, 800))
        self.add_widget(self.background_image)
        self.background_image.bind(size=self.update_labels)

        if 5 <= competitors_no <= 8:
            if not "contestant_no" in self.participants_dataframe:
                random_permutation = np.array([*range(1, len(self.participants_dataframe) + 1)])
                np.random.shuffle(random_permutation)
                self.participants_dataframe.insert(0, "contestant_no", random_permutation)
                self.participants_dataframe = self.participants_dataframe.sort_values(by=['contestant_no'])

            if len(self.labels) == 0:
                self.create_competitors_labels()
            self.update_labels()

    def create_competitors_labels(self):
        for i in range(1, 9):
            bracket = (i + 1) // 2
            position = 1 if i % 2 else 2

            if len(self.participants_dataframe) > i - 1:
                text = (self.participants_dataframe['name'].iloc[i - 1] +
                        '\n' +
                        self.participants_dataframe['surname'].iloc[i - 1])

                label = BackgroundLabel(text=text, color=(0, 0, 0, 1), size_hint=(None, None), size=(162, 52))
                self.labels[f'b1_{bracket}_{position}'] = label
                self.add_widget(label)

            else:
                label = BackgroundLabel(text="-", color=(0, 0, 0, 1), size_hint=(None, None), size=(162, 52))
                self.labels[f'b1_{bracket}_{position}'] = label
                self.add_widget(label)

    def update_labels(self, *args):

        center_x = self.width / 2
        center_y = self.height / 2
        left_bottom_x, left_bottom_y = self.to_window(self.x, self.y)

        repechage = "r" if self.repechage else "b"
        for level in range(1, 4):
            for bracket in range(1, 5):
                for position in range(1, 3):
                    label = self.labels[f"{repechage}{level}_{bracket}_{position}"]
                    pos = self.positions[f"{repechage}{level}_{bracket}_{position}"]

                    if label and pos:
                        label.pos = (left_bottom_x + center_x + pos['x'],
                                     left_bottom_y + center_y + pos['y'])


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