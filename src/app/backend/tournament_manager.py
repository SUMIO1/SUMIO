import logging
from collections import defaultdict
from typing import DefaultDict

import pandas as pd
import numpy as np


class TournamentManager:
    def __init__(self, chosen_participants: pd.DataFrame):
        logging.info("Initializing new tournament")
        self.contestants: pd.DataFrame = chosen_participants

        # the way to address participants in the tree:
        # b1_3_2 - level 1, bracket 3, position 2
        self.contestants_in_the_normal_tree: DefaultDict[str, pd.Series] = defaultdict(None)
        self.contestants_in_the_repechage_tree: DefaultDict[str, pd.Series] = defaultdict(None)

        # initialize the tournament
        self.permutate_contestants()
        self.assign_contestants_to_the_tree()

    def permutate_contestants(self):
        random_permutation = np.array(
            [*range(1, len(self.contestants) + 1)]
        )
        np.random.shuffle(random_permutation)
        self.contestants.insert(
            0, "contestant_no", random_permutation
        )
        self.contestants = self.contestants.sort_values(
            by=["contestant_no"]
        )

    # point to the winner by giving their level, bracket and participant number
    def designate_a_winner(self, level: int, bracket: int, participant: int):
        winner_key = f"b{level}_{bracket}_{participant}"
        contestant = self.contestants_in_the_normal_tree[winner_key]

        new_key = f"b{level + 1}_{(bracket - 1) % 2 + 1}_{(bracket + 1) % 2 + 1}"
        self.contestants_in_the_normal_tree[new_key] = contestant

    def get_contestants_tree(self, repechage: bool):
        if repechage:
            return self.contestants_in_the_repechage_tree
        return self.contestants_in_the_normal_tree

    def get_num_of_competitors(self) -> int:
        return len(self.contestants)

    def assign_contestants_to_the_tree(self):
        for i in range(1, 9):
            bracket = (i + 1) // 2
            position = 1 if i % 2 else 2

            if len(self.contestants) > i - 1:
                key = f"b1_{bracket}_{position}"
                self.contestants_in_the_normal_tree[key] = self.contestants.iloc[i - 1]
