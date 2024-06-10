import pandas as pd


class ParticipantsManager:
    def __init__(self):
        self.chosen_participants = pd.DataFrame()

    def clear(self):
        self.chosen_participants = pd.DataFrame()

    def add(self, participant):
        self.chosen_participants = pd.concat(
            [self.chosen_participants, participant.to_frame().T]
        )

    def remove(self, participant):
        self.chosen_participants = self.chosen_participants.drop(participant.name)

    def is_selected(self, participant):
        if any(
            self.chosen_participants.iloc[i, :].equals(participant)
            for i in range(len(self.chosen_participants))
        ):
            return True
        return False

    def length(self):
        return len(self.chosen_participants)

    def toggle(self, participant):
        if self.is_selected(participant):
            self.chosen_participants = self.chosen_participants.drop(participant.name)
            return False
        else:
            self.chosen_participants = pd.concat(
                [self.chosen_participants, participant.to_frame().T]
            )
            return True
