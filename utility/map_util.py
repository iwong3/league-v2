# map.py stores helper functions to map various Riot API constants

import json

# champion name
def get_champion_name(champ_id):

    # load champions map
    with open("utility/maps/champions.json", encoding="utf8") as file:
        champion_json = json.load(file)
        champion_data = champion_json.get("data")

    # get champion name
    champion_name = "n/a"
    for champion in champion_data:
        if champion_data[champion]["key"] == str(champ_id):
            champion_name = champion_data[champion]["name"]

    return champion_name

# league map names
def get_league_map_name(league_map_id):

    # load league maps mapping
    with open("utility/maps/league_maps.json", encoding="utf8") as file:
        league_maps_json = json.load(file)

    # get map name
    league_map_name = "n/a"
    for league_map in league_maps_json:
        if league_map.get("mapId") == league_map_id:
            league_map_name = league_map.get("mapName")

    return league_map_name

# queue description
def get_queue(queue_id):

    # load queues map
    with open("utility/maps/queues.json", encoding="utf8") as file:
        queues_json = json.load(file)

    # get queue description
    queue_description = "n/a"
    for queue in queues_json:
        if queue.get("queueId") == queue_id:
            queue_description = queue.get("description")

    return queue_description

# season
def get_season(season_id):

    # load seasons map
    with open("utility/maps/seasons.json", encoding="utf8") as file:
        seasons_json = json.load(file)

    # get season name
    season_name = "n/a"
    for season in seasons_json:
        if season.get("id") == season_id:
            season_name = season.get("season")

    return season_name
