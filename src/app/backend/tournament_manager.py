import logging
from collections import defaultdict
from typing import DefaultDict, Optional

import pandas as pd
import numpy as np


class TournamentManager:
    def __init__(self, chosen_participants: pd.DataFrame):
        logging.info("Initializing new tournament")
        self.contestants: pd.DataFrame = chosen_participants
        self.tournament_has_stared = False
        self.duels_manager_normal: Optional[DuelsManager] = None
        self.duels_manager_repechage: Optional[DuelsManager] = None

        # the way to address participants in the tree:
        # b1_3_2 - level 1, bracket 3, position 2
        self.contestants_in_the_normal_tree: DefaultDict[str, pd.Series] = defaultdict(None)
        self.contestants_in_the_repechage_tree: DefaultDict[str, pd.Series] = defaultdict(None)

        # initialize the tournament
        self.__permutate_contestants()
        self.__initialize_contestants_int_the_normal_tree()

    def __permutate_contestants(self):
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

    def swap_contestants(self, key1, key2):
        self.contestants_in_the_normal_tree[key1], self.contestants_in_the_normal_tree[key2] = self.contestants_in_the_normal_tree[key2], self.contestants_in_the_normal_tree[key1]

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

    def __initialize_contestants_int_the_normal_tree(self):
        for i in range(1, 9):
            bracket = (i + 1) // 2
            position = 1 if i % 2 else 2

            if len(self.contestants) > i - 1:
                key = f"b1_{bracket}_{position}"
                self.contestants_in_the_normal_tree[key] = self.contestants.iloc[i - 1]

    def start_the_tournament(self):
        self.tournament_has_stared = True
        self.duels_manager_normal = DuelsManager(
            self.contestants_in_the_normal_tree,
            self.contestants_in_the_repechage_tree,
            self.get_num_of_competitors(),
            False)
        self.duels_manager_repechage = DuelsManager(
            self.contestants_in_the_normal_tree,
            self.contestants_in_the_repechage_tree,
            self.get_num_of_competitors(),
            True)
        logging.info("Tournament has started")


class DuelsManager:
    def __init__(self,
                 contestants_normal_tree: DefaultDict[str, pd.Series],
                 contestants_repechage_tree: DefaultDict[str, pd.Series],
                 num_of_contestants,
                 repechage: bool):
        # fighter 1, fighter 2, where to write the winner (normal), where to write the looser (repechage)
        self.duels: list[tuple[str, str, str, Optional[str]]] = []
        self.contestants_in_the_normal_tree = contestants_normal_tree
        self.contestants_in_the_repechage_tree = contestants_repechage_tree
        self.num_of_contestants = num_of_contestants

        if repechage:
            self.__generate_repechage_duels()
        else:
            self.__generate_normal_duels()
        print(self.duels)

    def __generate_normal_duels(self):
        if self.num_of_contestants == 2:
            raise NotImplementedError()

        elif 3 <= self.num_of_contestants <= 4:
            raise NotImplementedError()

        elif 5 <= self.num_of_contestants <= 8:
            self.duels.extend([
                ("b1_1_1", "b1_1_2", "b2_1_1", "r1_1_1"),
                ("b1_2_1", "b1_2_2", "b2_1_2", "r1_1_2"),
                ("b1_3_1", "b1_3_2", "b2_2_1", "r1_2_1"),
                ("b1_4_1", "b1_4_2", "b2_2_2", "r1_2_2"),
                ("b2_1_1", "b2_1_2", "b3_1_1", "r2_1_!"),
                ("b2_2_1", "b2_2_2", "b3_1_2", "r2_2_2"),
                ("b3_1_1", "b3_1_2", "1st_place", "2nd_place")
            ])

        elif 9 <= self.num_of_contestants <= 16:
            raise NotImplementedError()

        else:
            raise ValueError("Could not generate order of duels. Invalid number of contestants.")

    def __generate_repechage_duels(self):
        if self.num_of_contestants == 2:
            raise NotImplementedError()

        elif 3 <= self.num_of_contestants <= 4:
            raise NotImplementedError()

        elif 5 <= self.num_of_contestants <= 8:
            self.duels.extend([
                ("r1_1_1", "r1_1_2", "r2_1_2", None),
                ("r1_2_1", "r1_2_2", "r2_2_1", None),
                ("r2_1_1", "r2_1_2", "r3_1_1", None),
                ("r2_2_1", "r2_2_2", "r3_1_2", None),
                ("r3_1_1", "r3_1_2", "3rd_place", None),
            ])

        elif 9 <= self.num_of_contestants <= 16:
            raise NotImplementedError()

        else:
            raise ValueError("Could not generate order of duels. Invalid number of contestants.")

