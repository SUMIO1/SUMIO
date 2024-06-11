

class BracketEditor:
    def __init__(self, tournament_manager):
        self.edit_mode = False
        self.chosen_label = None
        self.tournament_manager = tournament_manager

    def toggle_edit_mode(self, label, touch):
        if 410 < touch.pos[0] < 410 + 162 and 840 < touch.pos[1] < 840 + 52:
            if self.chosen_label is not None:
                self.chosen_label.update_color(1, 1, 1, 1)
            if self.edit_mode is False:
                self.edit_mode = True
                label.update_color(.7, 1, .7, 1)

            else:
                self.edit_mode = False
                label.update_color(.7, .7, .7, 1)

    def on_click(self, label, touch):
        print(touch.pos)
        if self.edit_mode is False or self.tournament_manager.tournament_has_stared:
            self.edit_mode = False
            return

        if label.pos[0] < touch.pos[0] < label.pos[0] + 162 and label.pos[1] < touch.pos[1] < label.pos[1] + 52:
            if self.chosen_label is None:
                self.chosen_label = label
                label.update_color(0, 1, 0, .2)
            elif self.chosen_label == label:
                self.chosen_label = None
                label.update_color(1, 1, 1, 1)
            else:
                self.chosen_label.text, label.text = label.text, self.chosen_label.text
                self.tournament_manager.swap_contestants(self.chosen_label.key, label.key)
                self.chosen_label.update_color(1, 1, 1, 1)
                self.chosen_label = None


