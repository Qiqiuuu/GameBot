from typing import List, Dict, Union

import discord


def writePlayersInLobby(players: Union[List, Dict]):
    str = ""
    if isinstance(players, list):
        for i in players:
            str += i.mention + "\n"
    elif isinstance(players, dict):
        for key, val in players.items():
            if isinstance(val, discord.PartialEmoji):
                str += val.name + " " + key.mention + "\n"
            else:
                str += val + " " + key.mention + "\n"
    return str
