import config
import requests
import json
import ast
import numpy as np
import pandas as pd

method_dict = {"GetNewsForApp": "ISteamNews/GetNewsForApp/v0002/",
               "GetGlobalAchievementPercentagesForApp": "ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/",
               "GetGlobalStatsForGame": "ISteamUserStats/GetGlobalStatsForGame/v0001/",
               "GetPlayerSummaries": "ISteamUser/GetPlayerSummaries/v0002/",
               "GetFriendList": "ISteamUser/GetFriendList/v0001/",
               "GetPlayerAchievements": "ISteamUserStats/GetPlayerAchievements/v0001/",
               "GetUserStatsForGame": "ISteamUserStats/GetUserStatsForGame/v0002/",
               "GetOwnedGames": "IPlayerService/GetOwnedGames/v0001/",
               "GetRecentlyPlayedGames": "IPlayerService/GetRecentlyPlayedGames/v0001/",
               "IsPlayingSharedGame": "IPlayerService/IsPlayingSharedGame/v0001/",
               "GetSchemaForGame": "ISteamUserStats/GetSchemaForGame/v2/",
               "GetPlayerBans": "ISteamUser/GetPlayerBans/v1/"
               }

# GetOwnedGames accepts a Steam user id and queries the Steam Web API to retrieve information about the user's owned games
# Functions are provided to gather limited insights from the retrieved data

# Example usage
# player_one = SteamProfile(config.steam_user)
# player_one.count_games()
# player_one.count_played()
# player_one.percent_played()
# player_one.top_ten()


class SteamProfile():
    def __init__(self, steam_id):
        self.steam_id = steam_id
        fetch_url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}".format(
            config.api_key, self.steam_id)
        self.r = requests.get(fetch_url)
        self.data = self.r.json()

    def count_games(self):
        self.games_owned = self.data["response"]["game_count"]
        print("Number of games owned: " + str(self.games_owned))

    def count_played(self):
        self.list = []
        for i in self.data["response"]["games"][0:-1]:
            if i["playtime_forever"] > 0:
                self.list.append(i)

        self.played = len(self.list)
        print("Number of games played: " + str(self.played))

    def percent_played(self):
        self.percent = self.played / self.games_owned
        print("Percentage of owned games that have been played: " + str(self.percent))

    def top_ten(self):
        self.playtime_sorted = json.dumps(sorted(self.data["response"]["games"], key=lambda i: i["playtime_forever"], reverse=True), indent=4)
        self.top_ten = ast.literal_eval(self.playtime_sorted)[:10]

        for i in self.top_ten:
            self.titles = []
            self.appid = i["appid"]
            self.appid_url = "http://store.steampowered.com/api/appdetails?appids={0}".format(
                self.appid)
            self.r = requests.get(self.appid_url)
            self.app_data = self.r.json()
            if json.dumps(self.app_data[str(self.appid)]["success"]) == "false":
                self.titles.append("No data....")
            else:
                self.titles.append(json.dumps(
                    self.app_data[str(self.appid)]["data"]["name"], indent=4))

            for x in self.titles:
                print(x)
