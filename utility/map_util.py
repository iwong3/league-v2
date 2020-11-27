# map.py stores helper functions to map various Riot API constants

import json


def get_champion_name(champ_id):

    # load champion map
    with open("utility/maps/champions.json", encoding="utf8") as file:
        champion_json = json.load(file)
        champion_data = champion_json["data"]

    # get champion name
    champion_name = "n/a"
    for champion in champion_data:
        if champion_data[champion]["key"] == str(champ_id):
            champion_name = champion_data[champion]["name"]

    return champion_name
