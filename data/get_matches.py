from dotenv import load_dotenv
from ratelimit import limits, sleep_and_retry

import os
import requests
import sqlite3
import time

# hack to import from outside of /data folder (b/c we have everything in one repo)
import sys
sys.path.append("../")
from utility import constants


# load env vars
load_dotenv()

# init riot api endpoint vars
# key
RIOT_API_KEY = os.environ.get("riot-api-key")
# endpoints
NA_ENDPOINT = "https://na1.api.riotgames.com"
SUMMONER_BY_NAME_PATH = "/lol/summoner/v4/summoners/by-name/"
MATCHLIST_BY_ACCOUNT_PATH = "/lol/match/v4/matchlists/by-account/"
MATCH_BY_ID_PATH = "/lol/match/v4/matches/"
# requests
request_headers = { "X-Riot-Token": RIOT_API_KEY }
# rate limiting
RATE_LIMIT_CALLS = 80
RATE_LIMIT_DURATION = 120 # 2 minutes

# db constants
MAX_MATCHES_TO_INSERT = 10000
REPOPULATE_FLAG = False

# for printing calls
count = 1


# Steps:
# 1. set up list of account_ids and list of match_ids to query
# 2. get your account id from summoner name (summoner endpoint) and add to list of account_ids
# 3. get your match list from your account id (matches endpoint) and add all match_ids to list of match_ids
# 4. while list of match_ids > 0:
#    - get match data from match endpoint
#    - get list of participants, add account_ids to list of account_ids
#    - get data for db, format, insert into db (error handling for dups)
# 5. if no more match ids, pop from list of account_ids and repeat from 3.
# 6. if no more account_ids, yikes (repeat on randomly selected summoner name)
def get_matches(summoner_name):

    # connect to database
    db_name = "C:/Users/Ivan/Coding/sqlite/league.db"
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # account ids and match ids to query
    account_ids = []
    match_ids = []
    matches_inserted = 0

    # get initial account id
    summoner_request_url = NA_ENDPOINT + SUMMONER_BY_NAME_PATH + summoner_name
    summoner_response_data = call_api(summoner_request_url, request_headers).json()
    account_id = summoner_response_data["accountId"]
    account_ids.append(account_id)

    # for all account ids
    while len(account_ids) > 0 and matches_inserted < MAX_MATCHES_TO_INSERT:

        # get matchlist
        account_id = account_ids.pop()
        matchlist_request_url = NA_ENDPOINT + MATCHLIST_BY_ACCOUNT_PATH + account_id
        matchlist_response_data = call_api(matchlist_request_url, request_headers)
        if matchlist_response_data == None or matchlist_response_data.json().get("matches") == None:
            matchlist = []
        else:
            matchlist = matchlist_response_data.json().get("matches")

        # add all match ids from matchlist that haven't not already been stored, unless re-populating
        for match in matchlist:
            match_id = match["gameId"]
            if REPOPULATE_FLAG:
                match_ids.append(match_id)
            else:
                cursor.execute("SELECT id FROM {} WHERE id = ?".format(constants.MATCH_TABLE_NAME), (match_id,))
                data = cursor.fetchone()
                if data is None:
                    match_ids.append(match_id)

        # for all match ids
        while len(match_ids) > 0 and matches_inserted < MAX_MATCHES_TO_INSERT:

            # get match
            match_id = match_ids.pop()
            match_request_url = NA_ENDPOINT + MATCH_BY_ID_PATH + str(match_id)
            match_response_data = call_api(match_request_url, request_headers).json()

            curr_match_id = match_response_data.get("gameId")

            # insert into Match table
            match_sql = (
                "INSERT INTO {} "
                "(id, game_creation, game_duration, game_mode, game_type, game_version,"
                " map_id, queue_id, season_id)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)".format(constants.MATCH_TABLE_NAME)
            )
            try:
                cursor.execute(match_sql, (
                    curr_match_id, match_response_data.get("gameCreation"),
                    match_response_data.get("gameDuration"), match_response_data.get("gameMode"),
                    match_response_data.get("gameType"), match_response_data.get("gameVersion"),
                    match_response_data.get("mapId"), match_response_data.get("queueId"), match_response_data.get("seasonId")
                ))
            except Exception as e:
                print(e)

            # insert into MatchTeam table
            match_team_sql = (
                "INSERT INTO {} "
                "(match_id, team_id, win,"
                " total_kills, total_deaths, total_assists,"
                " total_physical_damage_dealt, total_magic_damage_dealt, total_true_damage_dealt, total_damage_dealt,"
                " total_physical_damage_dealt_to_champions, total_magic_damage_dealt_to_champions,"
                " total_true_damage_dealt_to_champions, total_damage_dealt_to_champions,"
                " total_physical_damage_taken, total_magic_damage_taken, total_true_damage_taken, total_damage_taken,"
                " total_damage_self_mitigated,"
                " total_heal,"
                " total_minions_killed, total_neutral_minions_killed,"
                " total_neutral_minions_killed_team_jungle, total_neutral_minions_killed_enemy_jungle,"
                " total_time_crowd_control_dealt, total_time_ccing_others,"
                " total_damage_dealt_to_turrets, total_damage_dealt_to_objectives,"
                " total_gold_earned, total_gold_spent,"
                " total_vision_score, total_vision_wards_bought_in_game, total_wards_killed, total_wards_placed,"
                " first_blood, first_baron, first_dragon, first_inhibitor, first_rift_herald, first_tower,"
                " baron_kills, dragon_kills, inhibitor_kills, rift_herald_kills, tower_kills,"
                " champion_ban_1, champion_ban_2, champion_ban_3, champion_ban_4, champion_ban_5)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(constants.MATCH_TEAM_TABLE_NAME)
            )
            # one for each team in match
            for team in match_response_data.get("teams"):
                # set up team totals
                curr_team_id = team.get("teamId")
                # kda
                total_kills, total_deaths, total_assists = 0, 0, 0
                # dmg dealt/taken
                total_physical_damage_dealt, total_magic_damage_dealt, total_true_damage_dealt, total_damage_dealt = 0, 0, 0, 0
                total_physical_damage_dealt_to_champions, total_magic_damage_dealt_to_champions = 0, 0
                total_true_damage_dealt_to_champions, total_damage_dealt_to_champions = 0, 0
                total_physical_damage_taken, total_magic_damage_taken, total_true_damage_taken, total_damage_taken = 0, 0, 0, 0
                total_damage_self_mitigated = 0
                # healing
                total_heal = 0
                # cs
                total_minions_killed, total_neutral_minions_killed = 0, 0
                total_neutral_minions_killed_team_jungle, total_neutral_minions_killed_enemy_jungle = 0, 0
                # cc
                total_time_crowd_control_dealt, total_time_ccing_others = 0, 0
                # objectives
                total_damage_dealt_to_turrets, total_damage_dealt_to_objectives = 0, 0
                # gold
                total_gold_earned, total_gold_spent = 0, 0
                # vision & wards
                total_vision_score, total_vision_wards_bought_in_game, total_wards_killed, total_wards_placed = 0, 0, 0, 0

                for participant in match_response_data.get("participants"):
                    if curr_team_id == participant.get("teamId"):
                        curr_player_stats = participant.get("stats")
                        if curr_player_stats:
                            # kda
                            total_kills += curr_player_stats.get("kills")
                            total_deaths += curr_player_stats.get("deaths")
                            total_assists += curr_player_stats.get("assists")
                            # dmg dealt/taken
                            total_physical_damage_dealt += curr_player_stats.get("physicalDamageDealt")
                            total_magic_damage_dealt += curr_player_stats.get("magicDamageDealt")
                            total_true_damage_dealt += curr_player_stats.get("trueDamageDealt")
                            total_damage_dealt += curr_player_stats.get("totalDamageDealt")
                            total_physical_damage_dealt_to_champions += curr_player_stats.get("physicalDamageDealtToChampions")
                            total_magic_damage_dealt_to_champions += curr_player_stats.get("magicDamageDealtToChampions")
                            total_true_damage_dealt_to_champions += curr_player_stats.get("trueDamageDealtToChampions")
                            total_damage_dealt_to_champions += curr_player_stats.get("totalDamageDealtToChampions")
                            total_physical_damage_taken += curr_player_stats.get("physicalDamageTaken")
                            total_magic_damage_taken += curr_player_stats.get("magicalDamageTaken")
                            total_true_damage_taken += curr_player_stats.get("trueDamageTaken")
                            total_damage_taken += curr_player_stats.get("totalDamageTaken")
                            total_damage_self_mitigated += curr_player_stats.get("damageSelfMitigated")
                            # healing
                            total_heal += curr_player_stats.get("totalHeal")
                            # cs
                            total_minions_killed += curr_player_stats.get("totalMinionsKilled")
                            total_neutral_minions_killed += curr_player_stats.get("neutralMinionsKilled")
                            total_neutral_minions_killed_team_jungle += zero_if_none(curr_player_stats.get("neutralMinionsKilledTeamJungle"))
                            total_neutral_minions_killed_enemy_jungle += zero_if_none(curr_player_stats.get("neutralMinionsKilledEnemyJungle"))
                            # cc
                            total_time_crowd_control_dealt += curr_player_stats.get("totalTimeCrowdControlDealt")
                            total_time_ccing_others += curr_player_stats.get("timeCCingOthers")
                            # objectives
                            total_damage_dealt_to_turrets += curr_player_stats.get("damageDealtToTurrets")
                            total_damage_dealt_to_objectives += curr_player_stats.get("damageDealtToObjectives")
                            # gold
                            total_gold_earned += curr_player_stats.get("goldEarned")
                            total_gold_spent += curr_player_stats.get("goldSpent")
                            # vision & wards
                            total_vision_score += curr_player_stats.get("visionScore")
                            total_vision_wards_bought_in_game += curr_player_stats.get("visionWardsBoughtInGame")
                            total_wards_killed += zero_if_none(curr_player_stats.get("wardsKilled"))
                            total_wards_placed += zero_if_none(curr_player_stats.get("wardsPlaced"))

                # set up bans
                bans = team.get("bans")
                ban1, ban2, ban3, ban4, ban5 = None, None, None, None, None
                if bans:
                    for i in range(len(bans)):
                        if i == 0: ban1 = bans[i].get("championId")
                        if i == 1: ban2 = bans[i].get("championId")
                        if i == 2: ban3 = bans[i].get("championId")
                        if i == 3: ban4 = bans[i].get("championId")
                        if i == 4: ban5 = bans[i].get("championId")

                try:
                    cursor.execute(match_team_sql, (
                        curr_match_id, curr_team_id, team.get("win"),
                        total_kills, total_assists, total_deaths,
                        total_physical_damage_dealt, total_magic_damage_dealt, total_true_damage_dealt, total_damage_dealt,
                        total_physical_damage_dealt_to_champions, total_magic_damage_dealt_to_champions,
                        total_true_damage_dealt_to_champions, total_damage_dealt_to_champions,
                        total_physical_damage_taken, total_magic_damage_taken, total_true_damage_taken, total_damage_taken,
                        total_damage_self_mitigated,
                        total_heal,
                        total_minions_killed, total_neutral_minions_killed,
                        total_neutral_minions_killed_team_jungle, total_neutral_minions_killed_enemy_jungle,
                        total_time_crowd_control_dealt, total_time_ccing_others,
                        total_damage_dealt_to_turrets, total_damage_dealt_to_objectives,
                        total_gold_earned, total_gold_spent,
                        total_vision_score, total_vision_wards_bought_in_game, total_wards_killed, total_wards_placed,
                        team.get("firstBlood"), team.get("firstBaron"), team.get("firstDragon"),
                        team.get("firstInhibitor"), team.get("firstRiftHerald"), team.get("firstTower"),
                        team.get("baronKills"), team.get("dragonKills"), team.get("inhibitorKills"),
                        team.get("riftHeraldKills"), team.get("towerKills"),
                        ban1, ban2, ban3, ban4, ban5
                    ))
                except Exception as e:
                    print(e)

            # insert into MatchParticipants table
            match_participants_sql = (
                "INSERT INTO {} "
                "(match_id, participant_id, team_id, spell_1_id, spell_2_id, win,"
                " champion_id, champ_level, kills, deaths, assists, total_minions_killed,"
                " item_0, item_1, item_2, item_3, item_4, item_5, item_6,"
                " first_blood_kill, first_blood_assist,"
                " double_kills, triple_kills, quadra_kills, penta_kills, unreal_kills,"
                " largest_multi_kill, killing_sprees, largest_killing_spree,"
                " physical_damage_dealt, magic_damage_dealt, true_damage_dealt, total_damage_dealt,"
                " physical_damage_dealt_to_champions, magic_damage_dealt_to_champions,"
                " true_damage_dealt_to_champions, total_damage_dealt_to_champions, largest_critical_strike,"
                " physical_damage_taken, magic_damage_taken,"
                " true_damage_taken, total_damage_taken, damage_self_mitigated,"
                " total_heal, total_units_healed,"
                " neutral_minions_killed, neutral_minions_killed_team_jungle, neutral_minions_killed_enemy_jungle,"
                " total_time_crowd_control_dealt, time_ccing_others,"
                " first_tower_kill, first_tower_assist, turret_kills, damage_dealt_to_turrets,"
                " first_inhibitor_kill, first_inhibitor_assist, inhibitor_kills, damage_dealt_to_objectives,"
                " gold_earned, gold_spent, longest_time_spent_living,"
                " vision_score, vision_wards_bought_in_game, wards_killed, wards_placed,"
                " perk_primary_style,"
                " perk_0, perk_0_var_1, perk_0_var_2, perk_0_var_3,"
                " perk_1, perk_1_var_1, perk_1_var_2, perk_1_var_3,"
                " perk_2, perk_2_var_1, perk_2_var_2, perk_2_var_3,"
                " perk_3, perk_3_var_1, perk_3_var_2, perk_3_var_3,"
                " perk_sub_style,"
                " perk_4, perk_4_var_1, perk_4_var_2, perk_4_var_3,"
                " perk_5, perk_5_var_1, perk_5_var_2, perk_5_var_3,"
                " stat_perk_0, stat_perk_1, stat_perk_2)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(constants.MATCH_PARTICIPANTS_TABLE_NAME)
            )
            # one for each participant in match
            for p in match_response_data["participants"]:
                s = p.get("stats")
                if s == None:
                    continue
                try:
                    cursor.execute(match_participants_sql, (
                        curr_match_id, p.get("participantId"), p.get("teamId"),
                        p.get("spell1Id"), p.get("spell2Id"), s.get("win"),
                        p.get("championId"), s.get("champLevel"), s.get("kills"), s.get("deaths"), s.get("assists"), s.get("totalMinionsKilled"),
                        s.get("item0"), s.get("item1"), s.get("item2"), s.get("item3"), s.get("item4"), s.get("item5"), s.get("item6"),
                        s.get("firstBloodKill"), s.get("firstBloodAssist"),
                        s.get("doubleKills"), s.get("tripleKills"), s.get("quadraKills"), s.get("pentaKills"), s.get("unrealKills"),
                        s.get("largestMultiKill"), s.get("killingSprees"), s.get("largestKillingSpree"),
                        s.get("physicalDamageDealt"), s.get("magicDamageDealt"), s.get("trueDamageDealt"), s.get("totalDamageDealt"),
                        s.get("physicalDamageDealtToChampions"), s.get("magicDamageDealtToChampions"),
                        s.get("trueDamageDealtToChampions"), s.get("totalDamageDealtToChampions"), s.get("largestCriticalStrike"),
                        s.get("physicalDamageTaken"), s.get("magicalDamageTaken"),
                        s.get("trueDamageTaken"), s.get("totalDamageTaken"), s.get("damageSelfMitigated"),
                        s.get("totalHeal"), s.get("totalUnitsHealed"),
                        s.get("neutralMinionsKilled"), s.get("neutralMinionsKilledTeamJungle"), s.get("neutralMinionsKilledEnemyJungle"),
                        s.get("totalTimeCrowdControlDealt"), s.get("timeCCingOthers"),
                        s.get("firstTowerKill"), s.get("firstTowerAssist"), s.get("turretKills"), s.get("damageDealtToTurrets"),
                        s.get("firstInhibitorKill"), s.get("firstInhibitorAssist"), s.get("inhibitorKills"), s.get("damageDealtToObjectives"),
                        s.get("goldEarned"), s.get("goldSpent"), s.get("longestTimeSpentLiving"),
                        s.get("visionScore"), s.get("visionWardsBoughtInGame"), s.get("wardsKilled"), s.get("wardsPlaced"),
                        s.get("perkPrimaryStyle"),
                        s.get("perk0"), s.get("perk0Var1"), s.get("perk0Var2"), s.get("perk0Var3"),
                        s.get("perk1"), s.get("perk1Var1"), s.get("perk1Var2"), s.get("perk1Var3"),
                        s.get("perk2"), s.get("perk2Var1"), s.get("perk2Var2"), s.get("perk2Var3"),
                        s.get("perk3"), s.get("perk3Var1"), s.get("perk3Var2"), s.get("perk3Var3"),
                        s.get("perkSubStyle"),
                        s.get("perk4"), s.get("perk4Var1"), s.get("perk4Var2"), s.get("perk4Var3"),
                        s.get("perk5"), s.get("perk5Var1"), s.get("perk5Var2"), s.get("perk5Var3"),
                        s.get("statPerk0"), s.get("statPerk1"), s.get("statPerk2")
                    ))
                except Exception as e:
                    print(e)

            # commit current match data to db
            conn.commit()

            matches_inserted += 1

            # add participant account ids
            for participant in match_response_data["participantIdentities"]:
                account_id = participant["player"]["accountId"]
                account_ids.append(account_id)

    conn.close()


@sleep_and_retry
@limits(calls=RATE_LIMIT_CALLS, period=RATE_LIMIT_DURATION)
def call_api(url, headers):

    global count

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        # account id not found - probably old match and account id had been regenerated
        if response.status_code == 404 and MATCHLIST_BY_ACCOUNT_PATH in url:
            return None
        # try one more time after waiting on 503/504
        if response.status_code == 503 or response.status_code == 504:
            time.sleep(5)
            response = requests.get(url, headers=headers)
        else:
            raise Exception(url, "failed with", response.status_code)

    print("Call",count)
    count += 1

    return response

# helper method to check for nonetype and return zero
# some response fields aren't available in arams
def zero_if_none(data):
    if data is None:
        return 0
    return data


# some names
# Smackadummy, Vivilyn, Khayame, Ricefoxx, Faliteran
# Yiliang Peng, SentientAI, ASTROBOY99, Spica1, TSM Spica
if __name__ == "__main__":
    get_matches("Jhun")
