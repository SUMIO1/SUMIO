from src.app.backend.tournament_manager import TournamentManager
from tkinter import filedialog, messagebox


def __get_wrestler_fullname(tournament_manager: TournamentManager, wrestler_key) -> str:
    wrestler_data = tournament_manager.get_contestant_data(wrestler_key)
    if wrestler_data.any():
        return f"{wrestler_data['name']} {wrestler_data['surname']}, {wrestler_data['country']}"
    else:
        return "-"


def __process_medalists(tournament_manager: TournamentManager) -> str:
    result = ""
    result += f"1. {__get_wrestler_fullname(tournament_manager, '1st_place')}\n"
    result += f"2. {__get_wrestler_fullname(tournament_manager, '2nd_place')}\n"
    result += f"3. {__get_wrestler_fullname(tournament_manager, '3rd_place')}\n"
    return result


def __process_duels_list(duels_repechage, tournament_manager):
    result = ""
    for i, (wrestler1_key, wrestler2_key, winner_key, _) in enumerate(duels_repechage):
        wrestler1_fullname = __get_wrestler_fullname(tournament_manager, wrestler1_key)
        wrestler2_fullname = __get_wrestler_fullname(tournament_manager, wrestler2_key)
        winner_fullname = __get_wrestler_fullname(tournament_manager, winner_key)
        result += f"{i+1}. {wrestler1_fullname} vs {wrestler2_fullname}\n"
        result += f"\tWinner: {winner_fullname}\n"
    return result


def __get_text_report(tournament_manager: TournamentManager) -> str:
    result = ""

    result += "Medalists\n"
    result += __process_medalists(tournament_manager)

    result += "\nRegular duels\n"
    duels_normal = tournament_manager.duels_manager_normal
    if duels_normal and duels_normal.duels:
        result += __process_duels_list(duels_normal.duels, tournament_manager)

    result += "\nRepechage duels\n"
    duels_repechage = tournament_manager.duels_manager_repechage
    if duels_repechage and duels_repechage.duels:
        result += __process_duels_list(duels_repechage.duels, tournament_manager)

    return result


def generate_report(tournament_manager: TournamentManager):
    f = filedialog.asksaveasfile(mode='w', confirmoverwrite=True, defaultextension=".txt")
    if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
        return

    text2save = __get_text_report(tournament_manager)
    f.write(text2save)

    f.close()

    messagebox.showinfo("Success", "Report saved successfully")
