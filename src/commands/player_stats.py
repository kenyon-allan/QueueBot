import trueskill
import json
from typing import Any, Dict, List
from discord import ApplicationContext, Member, User
from exceptions import *


class RoleStat:
    """
    Tracks a player's stats across a specific role
    """

    def __init__(self, init_dict: Dict[str, Any] | None = None):
        if init_dict:
            self.games_played: int = init_dict["games_played"]
            self.games_won: int = init_dict["games_won"]
            self.rating: trueskill.Rating = trueskill.Rating(
                init_dict["rating"]["mu"], init_dict["rating"]["sigma"]
            )
        else:
            self.games_played: int = 0
            self.games_won: int = 0
            self.rating = trueskill.Rating()

    def convert_to_dict(self) -> Dict[str, float | str]:
        """Converts all fields to dictionaries to allow dumping to json"""
        outp = {}
        outp["games_played"] = self.games_played
        outp["games_won"] = self.games_won
        outp["rating"] = {
            "mu": self.rating.mu,
            "sigma": self.rating.sigma,
        }
        return outp

    def get_stats(self) -> Dict[str, float | str]:
        """Returns a dictionary of the player's stats"""
        if self.games_played != 0:
            return {
                "games_played": self.games_played,
                "games_won": self.games_won,
                "win_rate": str(self.games_won / self.games_played * 100) + "%",
            }
        else:
            return {
                "games_played": 0,
                "games_won": 0,
                "win_rate": "0%",
            }


class PlayerStats:
    """
    Container class for player stats across multiple roles
    """

    def __init__(self, init_dict: Dict[str, Any] | None = None):
        if init_dict:
            self.tank = RoleStat(init_dict["tank"])
            self.support = RoleStat(init_dict["support"])
            self.assassin = RoleStat(init_dict["assassin"])
            self.offlane = RoleStat(init_dict["offlane"])
        else:
            self.tank = RoleStat()
            self.support = RoleStat()
            self.assassin = RoleStat()
            self.offlane = RoleStat()

    def convert_to_dict(self) -> Dict[str, float | str]:
        """Converts all fields to dictionaries to allow dumping to json"""
        outp = {}
        outp["tank"] = self.tank.convert_to_dict()
        outp["support"] = self.support.convert_to_dict()
        outp["assassin"] = self.assassin.convert_to_dict()
        outp["offlane"] = self.offlane.convert_to_dict()
        return outp


def load_player_data() -> None:
    """Loads player_data.json into memory for manipulation"""
    with open("player_data.json", "r") as f:
        dict_load = json.load(f)
        for key, value in dict_load.items():
            dict_load[key] = PlayerStats(value)
        global PLAYER_DATA
        PLAYER_DATA = dict_load


PLAYER_DATA: Dict[str, PlayerStats] = {}
load_player_data()


def update_player_data() -> None:
    """Updates player_data.json with the current data in memory"""
    with open("player_data.json", "w") as f:
        data_copy = PLAYER_DATA.copy()
        outp_dict: Dict[str, Dict[str, float | str]] = {}
        for key, value in data_copy.items():
            outp_dict[key] = value.convert_to_dict()
        json.dump(data_copy, f)
    load_player_data()


def instantiate_new_players(users: List[Member]) -> None:
    for user in users:
        if user.id not in PLAYER_DATA:
            PLAYER_DATA[str(user.id)] = PlayerStats()
    update_player_data()


def get_player_stats(ctx: ApplicationContext) -> Dict[str, Dict[str, float]]:
    """Returns the player's stats"""
    assert type(ctx.user) is Member
    if str(ctx.user.id) not in PLAYER_DATA:
        instantiate_new_players([ctx.user])
    user_data = PLAYER_DATA[str(ctx.user.id)]
    returned_stats = {}
    returned_stats["tank"] = user_data.tank.get_stats()
    returned_stats["support"] = user_data.support.get_stats()
    returned_stats["assassin"] = user_data.assassin.get_stats()
    returned_stats["offlane"] = user_data.offlane.get_stats()
    return returned_stats