import pandas as pd
from kivy.properties import StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from src.app.gui.pretty_button import PrettyButton  # noqa: F401


class WrestlerProfile(BoxLayout):
    def __init__(
        self, wrestler_data: pd.Series, wrestler_status, participants, **kwargs
    ):
        super().__init__(**kwargs)
        self.wrestler_data = wrestler_data

        self.ids["name_surname"].text = (
            "Participant: " + wrestler_data["name"] + " " + wrestler_data["surname"]
        )
        self.ids["age_category"].text = "Age Category: " + wrestler_data["age_category"]
        self.ids["date_of_birth"].text = (
            "Date of Birth: " + wrestler_data["date_of_birth"]
        )
        self.ids["age"].text = "Age: " + str(wrestler_data["age"])
        self.ids["weight_category"].text = "Weight: " + wrestler_data["weight_category"]
        self.ids["weight"].text = "Weight: " + str(wrestler_data["weight"]) + " kg"
        self.ids["country"].text = "Country: " + wrestler_data["country"]

        self.ids["image"].source = "https://picsum.photos/250"

        # temporary, just to check if buttons work
        def toggle_participant(button):
            status = participants.toggle(wrestler_data)
            wrestler_status.toggle(status)

        def callback(instance):
            print("Button pressed: " + str(instance))

        self.ids["btn_edit_profile"].bind(on_press=callback)
        self.ids["btn_add_to_tournament"].bind(on_press=toggle_participant)


class WrestlerSelectedStatus(AnchorLayout):
    # to change what is shown in the gui, simply change the value of the property below
    participation_message = StringProperty(
        "THIS PARTICIPANT IS [b]NOT[/b] SELECTED FOR THE TOURNAMENT"
    )

    def __init__(self, selected, **kwargs):
        super().__init__(**kwargs)
        self.selected = False
        self.toggle(selected)

    def toggle(self, status):
        self.selected = status
        if self.selected:
            self.participation_message = (
                "THIS PARTICIPANT IS SELECTED FOR THE TOURNAMENT"
            )
        else:
            self.participation_message = (
                "THIS PARTICIPANT IS [b]NOT[/b] SELECTED FOR THE TOURNAMENT"
            )


class WrestlerInfo(Label):
    pass
