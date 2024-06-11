from collections import defaultdict
from typing import DefaultDict, Dict

from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem

from src.app.backend.bracket_editor import BracketEditor
from src.app.backend.tournament_manager import TournamentManager
from src.app.gui.background_label import BackgroundLabel


class TabbedCompetition(TabbedPanel):
    def __init__(
            self,
            tournament_manager: TournamentManager,
            **kwargs,
    ):
        super(TabbedCompetition, self).__init__(**kwargs)
        self.tournament_manager = tournament_manager

        self.regular_bracket_tab = TabbedPanelItem(text="Bracket")
        self.regular_bracket_tab.add_widget(
            CompetitionBracket(
                tournament_manager=tournament_manager
            )
        )
        self.add_widget(self.regular_bracket_tab)

        self.repechage_bracket_tab = TabbedPanelItem(text="Repechage")
        self.repechage_bracket_tab.add_widget(
            CompetitionBracket(
                tournament_manager=tournament_manager,
                repechage=True,
            )
        )
        self.add_widget(self.repechage_bracket_tab)


class CompetitionBracket(FloatLayout):
    def __init__(
            self,
            tournament_manager: TournamentManager,
            repechage: bool = False,
            **kwargs,
    ):
        super(CompetitionBracket, self).__init__(**kwargs)
        self.tournament_manager = tournament_manager
        self.editor = BracketEditor(tournament_manager)
        competitors_no = tournament_manager.get_num_of_competitors()

        self.repechage = repechage

        if self.repechage:
            if competitors_no == 2:
                background = "./resources/images/placeholder.png"
            elif 3 <= competitors_no <= 4:
                background = "./resources/images/placeholder.png"
            elif 5 <= competitors_no <= 8:
                background = "./resources/images/background_5_8_re.png"
            elif 9 <= competitors_no <= 16:
                background = "./resources/images/placeholder.png"
            else:
                background = "./resources/images/placeholder.png"
        else:
            if competitors_no == 2:
                background = "./resources/images/placeholder.png"
            elif 3 <= competitors_no <= 4:
                background = "./resources/images/placeholder.png"
            elif 5 <= competitors_no <= 8:
                background = "./resources/images/background_5_8.png"
            elif 9 <= competitors_no <= 16:
                background = "./resources/images/placeholder.png"
            else:
                background = "./resources/images/placeholder.png"

        self.positions: DefaultDict[str, Dict[str, int]] = defaultdict(dict)

        self.positions.update(
            {
                "b1_1_1": {"x": -380, "y": 195},
                "b1_1_2": {"x": -380, "y": 140},
                "b1_2_1": {"x": -380, "y": -192},
                "b1_2_2": {"x": -380, "y": -246},
                "b1_3_1": {"x": 213, "y": 195},
                "b1_3_2": {"x": 213, "y": 140},
                "b1_4_1": {"x": 213, "y": -192},
                "b1_4_2": {"x": 213, "y": -246},
                "b2_1_1": {"x": -280, "y": -1},
                "b2_1_2": {"x": -280, "y": -55},
                "b2_2_1": {"x": 123, "y": -1},
                "b2_2_2": {"x": 123, "y": -55},
                "b3_1_1": {"x": -78, "y": -1},
                "b3_1_2": {"x": -78, "y": -55},
            }
        )

        self.positions.update(
            {
                "r1_1_1": {"x": -304, "y": 295},
                "r1_1_2": {"x": -304, "y": 240},
                "r1_2_1": {"x": -304, "y": -275},
                "r1_2_2": {"x": -304, "y": -332},
                "r2_1_1": {"x": -103, "y": 97},
                "r2_1_2": {"x": -103, "y": 42},
                "r2_2_1": {"x": -103, "y": -77},
                "r2_2_2": {"x": -103, "y": -135},
                "r3_1_1": {"x": 168, "y": 15},
                "r3_1_2": {"x": 168, "y": -41},
            }
        )

        self.background_image = Image(
            source=background,
            allow_stretch=False,
            keep_ratio=True,
            pos_hint={"x": 0, "y": 0},
            size=(800, 800),
        )
        self.add_widget(self.background_image)
        self.background_image.bind(size=self.update_labels)

        self.update_labels()

    def update_labels(self, *args):
        self.clear_widgets()
        self.add_widget(self.background_image)
        self.add_edit_button()
        labels = self.tournament_manager.get_contestants_tree(self.repechage)

        center_x = self.width / 2
        center_y = self.height / 2
        left_bottom_x, left_bottom_y = self.to_window(self.x, self.y)

        for key, contestant in labels.items():
            if not key.startswith("b") and not key.startswith("r"):  # skip other keys
                continue
            pos = self.positions[key]

            if contestant is not None:
                if contestant.any():
                    text = (
                            contestant["name"]
                            + "\n"
                            + contestant["surname"]
                    )
                else:
                    text = "-"

                label = BackgroundLabel(
                    text=text,
                    key=key,
                    color=(0, 0, 0, 1),
                    size_hint=(None, None),
                    size=(162, 52),
                    on_touch_down=self.editor.on_click
                )

            else:
                label = BackgroundLabel(
                    text="-",
                    key=key,
                    color=(0, 0, 0, 1),
                    size_hint=(None, None),
                    size=(162, 52)
                )

            label.pos = (
                left_bottom_x + center_x + pos["x"],
                left_bottom_y + center_y + pos["y"],
            )

            self.add_widget(label)

    def add_edit_button(self):
        if not self.tournament_manager.tournament_has_stared and self.repechage is False:
            self.add_widget(
                BackgroundLabel(
                    text="EDIT",
                    color=(0, 0, 0, 1),
                    size_hint=(None, None),
                    size=(162, 52),
                    on_touch_down=self.editor.toggle_edit_mode,
                    pos=(642.0, 840.0),
                    bg_color=(.7, .7, .7, 1)
                )
            )
        else:
            self.editor.edit_mode = False
