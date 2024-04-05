def writePlayersInLobby(list: list):
    str = ""
    for i in list:
        str+=i.mention+"\n"
    return str