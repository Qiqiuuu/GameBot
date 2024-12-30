import json
import os

import pandas
import requests
from dotenv import load_dotenv
load_dotenv()
STEAM_KEY = os.getenv('STEAM_API')

def SteamGetData(userIDs: dict):

    returnData = []

    for user in userIDs:
        games = requests.get(
        'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}&include_played_free_games=True&format=json'.format(
            STEAM_KEY, user)).text
        game = json.loads(games)

        for currGame in game["response"]["games"]:
            gameInfoReq = requests.get(
                'https://store.steampowered.com/api/appdetails?appids={}'.format(
                    currGame["appid"])).text
            gameInfoAns = json.loads(gameInfoReq)
            if gameInfoAns and str(currGame["appid"]) in gameInfoAns and gameInfoAns[str(currGame["appid"])]["success"]:
                game_info = gameInfoAns[str(currGame["appid"])]["data"]

                # Extract developers and categories safely
                developers = game_info.get("developers", [])
                categories = game_info.get("categories", [])
                returnData.append(
                    {
                        "UserID": user,
                        "AppID": currGame["appid"],
                        "PlaytimeForever": currGame.get("playtime_forever", 0),
                        "PlaytimeLastTwoWeeks": currGame.get("playtime_2weeks", 0),
                        "LastPlayed": currGame.get("rtime_last_played", 0),
                        "Developer": developers,
                        "Categories": [category["id"] for category in categories]
                    }
                )
    return returnData

print(SteamGetData([76561198165275140]))