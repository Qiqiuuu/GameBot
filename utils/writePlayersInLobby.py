from typing import List, Dict, Union


def writePlayersInLobby(players: Union[List, Dict]):
    str = ""
    if isinstance(players, list):
        for i in players:
            str += i.mention + "\n"
    elif isinstance(players, dict):
        for key, val in players.items():
            str += val + " " + key.mention + "\n"
    return str
