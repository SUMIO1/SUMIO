import logging
from collections import defaultdict
from typing import DefaultDict, Optional

import pandas as pd
import numpy as np


class TournamentManager:
    def __init__(self, chosen_participants: pd.DataFrame):
        logging.info("Initializing new tournament")
        self.__contestants: pd.DataFrame = chosen_participants
        self.tournament_has_stared = False
        self.tournament_has_finished = False
        self.duels_manager_normal: Optional[DuelsManager] = None
        self.duels_manager_repechage: Optional[DuelsManager] = None

        # the way to address participants in the tree:
        # b1_3_2 - level 1, bracket 3, position 2
        self.__contestants_in_the_normal_tree: DefaultDict[str, pd.Series] = defaultdict(pd.Series)
        self.__contestants_in_the_repechage_tree: DefaultDict[str, pd.Series] = defaultdict(pd.Series)
        self.__contestants_special: DefaultDict[str, pd.Series] = defaultdict(None)

        # initialize the tournament
        self.__permutate_contestants()
        self.__initialize_contestants_int_the_normal_tree()

    def __permutate_contestants(self):
        random_permutation = np.array(
            [*range(1, len(self.__contestants) + 1)]
        )
        np.random.shuffle(random_permutation)

        self.__contestants.insert(
            0, "contestant_no", random_permutation
        )
        self.__contestants = self.__contestants.sort_values(
            by=["contestant_no"]
        )

    def designate_a_winner(self, fight: tuple[str, str, str, Optional[str]], winner_key: str):
        if winner_key.startswith("b"):
            winner = self.__contestants_in_the_normal_tree[winner_key]
        elif winner_key.startswith("r"):
            winner = self.__contestants_in_the_repechage_tree[winner_key]
        else:
            raise ValueError(f"Invalid winner key: {winner_key}")

        if fight[2].startswith("b"):
            self.__contestants_in_the_normal_tree[fight[2]] = winner
        elif fight[2].startswith("r"):
            self.__contestants_in_the_repechage_tree[fight[2]] = winner
        else:
            self.__contestants_special[fight[2]] = winner

        looser_key = fight[0] if fight[0] != winner_key else fight[1]
        if looser_key.startswith("b"):
            looser = self.__contestants_in_the_normal_tree[looser_key]
        elif looser_key.startswith("r"):
            looser = self.__contestants_in_the_repechage_tree[looser_key]
        else:
            raise ValueError(f"Invalid looser key: {looser_key}")

        if fight[3]:
            if fight[3].startswith("b"):
                self.__contestants_in_the_normal_tree[fight[3]] = looser
            elif fight[3].startswith("r"):
                self.__contestants_in_the_repechage_tree[fight[3]] = looser
            else:
                self.__contestants_special[fight[3]] = looser

        self.get_next_duel()

    def get_contestants_tree(self, repechage: bool):
        if repechage:
            return self.__contestants_in_the_repechage_tree
        return self.__contestants_in_the_normal_tree

    def get_contestant_data(self, key: str):
        if key.startswith("b"):
            return self.__contestants_in_the_normal_tree[key]
        elif key.startswith("r"):
            return self.__contestants_in_the_repechage_tree[key]
        elif key in self.__contestants_special.keys():
            return self.__contestants_special[key]
        else:
            raise ValueError(f"Invalid key: {key}")

    def get_num_of_competitors(self) -> int:
        return len(self.__contestants)

    def __initialize_contestants_int_the_normal_tree(self):
        for i in range(1, 9):
            bracket = (i + 1) // 2
            position = 1 if i % 2 else 2

            if len(self.__contestants) > i - 1:
                key = f"b1_{bracket}_{position}"
                self.__contestants_in_the_normal_tree[key] = self.__contestants.iloc[i - 1]

    def start_the_tournament(self):
        self.tournament_has_stared = True
        self.duels_manager_normal = DuelsManager(
            self.__contestants_in_the_normal_tree,
            self.__contestants_in_the_repechage_tree,
            self.get_num_of_competitors(),
            False)
        self.duels_manager_repechage = DuelsManager(
            self.__contestants_in_the_normal_tree,
            self.__contestants_in_the_repechage_tree,
            self.get_num_of_competitors(),
            True)
        logging.info("Tournament has started")

    def finish_the_tournament(self):
        self.tournament_has_finished = True

    def get_next_duel(self) -> Optional[tuple[str, str, str, Optional[str]]]:
        if self.duels_manager_normal and self.duels_manager_normal.has_duels_left_to_fight():
            return self.duels_manager_normal.get_next_duel()

        if self.duels_manager_repechage and self.duels_manager_repechage.has_duels_left_to_fight():
            return self.duels_manager_repechage.get_next_duel()

        return None

    def peek_next_duel(self) -> Optional[tuple[str, str, str, Optional[str]]]:
        if self.duels_manager_normal is None or self.duels_manager_repechage is None:
            return None

        duel = self.duels_manager_normal.peek_next_duel()
        if duel:
            return duel

        duel = self.duels_manager_repechage.peek_next_duel()
        if duel:
            return duel

        return None

    def peek_next_next_duel(self):
        if self.duels_manager_normal is None or self.duels_manager_repechage is None:
            return None

        duel = self.duels_manager_normal.peek_next_next_duel()
        if duel:
            return duel

        # we are on the next to last duel of self.__duels_manager_normal
        elif self.duels_manager_normal.current_index + 1 == len(self.duels_manager_normal.duels):
            duel = self.duels_manager_repechage.peek_next_duel()
            return duel

        # we are on the last duel of self.__duels_manager_normal
        elif self.duels_manager_normal.current_index == len(self.duels_manager_normal.duels):
            duel = self.duels_manager_repechage.peek_next_next_duel()
            return duel

        return None

    def has_duels_left_to_fight(self) -> bool:
        if self.duels_manager_normal is None or self.duels_manager_repechage is None:
            return False

        return (
                self.duels_manager_normal.has_duels_left_to_fight()
                or
                self.duels_manager_repechage.has_duels_left_to_fight()
        )


class DuelsManager:
    def __init__(self,
                 contestants_normal_tree: DefaultDict[str, pd.Series],
                 contestants_repechage_tree: DefaultDict[str, pd.Series],
                 num_of_contestants,
                 repechage: bool):
        # fighter 1, fighter 2, where to write the winner (normal), where to write the looser (repêchage)
        self.duels: list[tuple[str, str, str, Optional[str]]] = []
        self.contestants_in_the_normal_tree = contestants_normal_tree
        self.contestants_in_the_repechage_tree = contestants_repechage_tree
        self.num_of_contestants = num_of_contestants

        self.current_index = 0

        if repechage:
            self.__generate_repechage_duels()
        else:
            self.__generate_normal_duels()

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
                ("b2_1_1", "b2_1_2", "b3_1_1", "r2_1_1"),
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

    def get_next_duel(self) -> Optional[tuple[str, str, str, Optional[str]]]:
        current_duel = self.duels[self.current_index]
        self.current_index += 1
        return current_duel

    def peek_next_duel(self) -> Optional[tuple[str, str, str, Optional[str]]]:
        if self.current_index < len(self.duels):
            return self.duels[self.current_index]
        return None

    def peek_next_next_duel(self) -> Optional[tuple[str, str, str, Optional[str]]]:
        if self.current_index + 1 < len(self.duels):
            return self.duels[self.current_index + 1]
        return None

    def has_duels_left_to_fight(self) -> bool:
        return self.current_index < len(self.duels)
