import pandas as pd
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from src.app.backend.tournament_manager import TournamentManager


class NextFightPreview(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_label(self, tournament_manager: TournamentManager, first_wrestler_key: str, second_wrestler_key: str):
        first_wrestler_data = tournament_manager.get_contestant_data(first_wrestler_key)
        second_wrestler_data = tournament_manager.get_contestant_data(second_wrestler_key)

        if first_wrestler_data.any():
            first_wrestler_fullname = f"{first_wrestler_data['name']} {first_wrestler_data['surname']}"
        else:
            first_wrestler_fullname = "-"

        if second_wrestler_data.any():
            second_wrestler_fullname = f"{second_wrestler_data['name']} {second_wrestler_data['surname']}"
        else:
            second_wrestler_fullname = "-"

        self.ids["label"].text = (f"Next fight: [b]{first_wrestler_fullname}[/b] "
                                  f"vs "
                                  f"[b]{second_wrestler_fullname}[/b]")

    def update_label_and_set_it_to_empty(self):
        self.ids["label"].text = "Next fight: [b]-[/b] vs [b]-[/b]"


class ChoosableWrestler(BoxLayout):
    def __init__(self, wrestler_data: pd.Series, on_contestant_win, **kwargs):
        super().__init__(**kwargs)
        self.ids["image"].source = "https://picsum.photos/250"

        if wrestler_data.any():
            self.ids["wrestler_name"].text = f"{wrestler_data['name']} {wrestler_data['surname']}, {wrestler_data['country']}"
        else:
            self.ids["wrestler_name"].text = "-"

        self.ids["choose_button"].bind(on_press=on_contestant_win)


class TournamentFight(BoxLayout):
    def __init__(self, tournament_manager: TournamentManager, next_fight_preview: NextFightPreview, **kwargs):
        super().__init__(**kwargs)

        self.tournament_manager = tournament_manager
        self.next_fight_preview = next_fight_preview

        self.vs_label = Label(
            text="vs",
            font_size=40,
            size_hint=(0.5, 1)
        )

        self.set_up_next_fight()

    def set_up_next_fight(self):
        self.ids["fight_content"].clear_widgets()

        duel = self.tournament_manager.peek_next_duel()
        # self.win_instantly_if_dueling_with_noone(duel)

        def on_left_contestant_win(*args):
            if duel is not None:
                self.tournament_manager.designate_a_winner(duel, duel[0])
                self.set_up_next_fight()

        def on_right_contestant_win(*args):
            if duel is not None:
                self.tournament_manager.designate_a_winner(duel, duel[1])
                self.set_up_next_fight()

        if duel is None:
            self.end_tournament()
            return

        left_wrestler = ChoosableWrestler(
            self.tournament_manager.get_contestant_data(duel[0]),
            on_left_contestant_win
        )

        right_wrestler = ChoosableWrestler(
            self.tournament_manager.get_contestant_data(duel[1]),
            on_right_contestant_win
        )

        self.ids["fight_content"].add_widget(left_wrestler)
        self.ids["fight_content"].add_widget(self.vs_label)
        self.ids["fight_content"].add_widget(right_wrestler)

        next_duel = self.tournament_manager.peek_next_next_duel()
        if next_duel is not None:
            self.next_fight_preview.update_label(self.tournament_manager, next_duel[0], next_duel[1])
        else:
            self.next_fight_preview.update_label_and_set_it_to_empty()

    def end_tournament(self):
        self.tournament_manager.finish_the_tournament()
