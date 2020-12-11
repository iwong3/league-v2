from flask import Blueprint, jsonify, request
from flask_cors import CORS

import json
import os
import sqlite3
import sys
import time

from utility import constants, map_util, sqlite_util


# flask setup
match_bp = Blueprint("match", __name__)

# constants
DEFAULT_ROW_LIMIT = 1000
DEFAULT_MAP_ID = 11


def get_blueprint():
    return match_bp


# /match/participants endpoint
@match_bp.route('/match/participants', methods=['GET'])
def get_match_participants():

    print("/match/participants endpoint hit")

    # read request args
    limit = request.args.get("limit", DEFAULT_ROW_LIMIT)

    # connect to database
    conn = sqlite3.connect(constants.PATH_TO_DB)
    cursor = conn.cursor()

    # set up response
    res = {
        "error": 0
    }

    # get query results
    sql = (
        "SELECT * FROM {} AS m "
        "INNER JOIN {} AS mp "
        "ON m.id = mp.match_id "
        "ORDER BY RANDOM() "
        "LIMIT {}"
    ).format(constants.MATCH_TABLE_NAME, constants.MATCH_PARTICIPANTS_TABLE_NAME, limit)
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        print(e)
        res["error"] = 1
        return jsonify(res)

    # close db conn after call
    conn.close()

    # set up response data
    res["data"] = []
    column_names = sqlite_util.get_column_names(cursor)

    # create response object for each row and add to response
    for row in rows:
        res_obj = {}
        for i in range(len(row)):
            curr_col_name = column_names[i]
            res_obj[curr_col_name] = row[i]
            # add extra field for id values that have mappings
            if "champion_id" == curr_col_name:
                res_obj["champion_name"] = map_util.get_champion_name(row[i])
            elif "map_id" == curr_col_name:
                res_obj["map_name"] = map_util.get_league_map_name(row[i])
            elif "queue_id" == curr_col_name:
                res_obj["queue_description"] = map_util.get_queue(row[i])
            elif "season_id" == curr_col_name:
                res_obj["season_name"] = map_util.get_season(row[i])
        res["data"].append(res_obj)

    return jsonify(res)


# /match/teams endpoint
@match_bp.route('/match/teams', methods=['GET'])
def get_match_teams():

    print("/match/teams endpoint hit")

    # read request args
    limit = request.args.get("limit", DEFAULT_ROW_LIMIT)

    # connect to database
    conn = sqlite3.connect(constants.PATH_TO_DB)
    cursor = conn.cursor()

    # set up response
    res = {
        "error": 0
    }

    # get query results
    sql = (
        "SELECT * FROM {} AS m "
        "INNER JOIN {} AS mt "
        "ON m.id = mt.match_id "
        "ORDER BY RANDOM() "
        "LIMIT {}"
    ).format(constants.MATCH_TABLE_NAME, constants.MATCH_TEAM_TABLE_NAME, limit)
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        print(e)
        res["error"] = 1
        return jsonify(res)

    # close db conn after call
    conn.close()

    # set up response data
    res["data"] = []
    column_names = sqlite_util.get_column_names(cursor)

    # create response object for each row and add to response
    for row in rows:
        res_obj = {}
        for i in range(len(row)):
            curr_col_name = column_names[i]
            res_obj[curr_col_name] = row[i]
            # add extra field for id values that have mappings
            if "map_id" == curr_col_name:
                res_obj["map_name"] = map_util.get_league_map_name(row[i])
            elif "queue_id" == curr_col_name:
                res_obj["queue_description"] = map_util.get_queue(row[i])
            elif "season_id" == curr_col_name:
                res_obj["season_name"] = map_util.get_season(row[i])
        res["data"].append(res_obj)

    return jsonify(res)


# /match/team-deltas endpoint
@match_bp.route('/match/team-deltas', methods=['GET'])
def get_match_team_deltas():

    print("/match/team-deltas endpoint hit")

    # read request args
    limit = request.args.get("limit", DEFAULT_ROW_LIMIT)
    map_id = request.args.get("map_id", DEFAULT_MAP_ID)

    # connect to database
    conn = sqlite3.connect(constants.PATH_TO_DB)
    cursor = conn.cursor()

    # set up response
    res = {
        "error": 0
    }

    # get query results
    sql = (
        "SELECT mt.match_id, mt.team_id, mt.win, "
        "mt.total_kills, mt.total_deaths, mt.total_assists, "
        "mt.total_physical_damage_dealt, mt.total_magic_damage_dealt, mt.total_true_damage_dealt, mt.total_damage_dealt, "
        "mt.total_physical_damage_dealt_to_champions, mt.total_magic_damage_dealt_to_champions, "
        "mt.total_true_damage_dealt_to_champions, mt.total_damage_dealt_to_champions, "
        "mt.total_physical_damage_taken, mt.total_magic_damage_taken, mt.total_true_damage_taken, mt.total_damage_taken, "
        "mt.total_damage_self_mitigated, "
        "mt.total_heal, "
        "mt.total_minions_killed, mt.total_neutral_minions_killed, "
        "mt.total_neutral_minions_killed_team_jungle, mt.total_neutral_minions_killed_enemy_jungle, "
        "mt.total_time_crowd_control_dealt, mt.total_time_ccing_others, "
        "mt.total_damage_dealt_to_turrets, mt.total_damage_dealt_to_objectives, "
        "mt.total_gold_earned, mt.total_gold_spent, "
        "mt.total_vision_score, mt.total_vision_wards_bought_in_game, mt.total_wards_killed, mt.total_wards_placed, "
        "mt.baron_kills, mt.dragon_kills, mt.inhibitor_kills, mt.rift_herald_kills, mt.tower_kills "
        "FROM {} AS m "
        "INNER JOIN {} AS mt "
        "ON m.id = mt.match_id "
        "WHERE m.id IN "
        "(SELECT id FROM {} ORDER BY RANDOM() LIMIT {}) "
        "AND m.map_id = {}"
    ).format(constants.MATCH_TABLE_NAME, constants.MATCH_TEAM_TABLE_NAME, constants.MATCH_TABLE_NAME, limit, map_id)
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        print(e)
        res["error"] = 1
        return jsonify(res)

    # close db conn after call
    conn.close()

    # hack way to handle async sql for now
    time.sleep(1)

    # set up response data
    res["data"] = []
    column_names = sqlite_util.get_column_names(cursor)
    team_deltas_data = []
    curr_match_id = rows[0][0]
    curr_match_win, curr_match_lose = None, None

    # populate response data
    for row in rows:
        # new match - process previous match data and reset curr vars
        if curr_match_id != row[0]:
            res_obj_win = {}
            res_obj_lose = {}
            # process previous match
            for i in range(len(curr_match_win)):
                curr_col_name = column_names[i]
                # non-delta fields
                if "match_id" == curr_col_name or "team_id" == curr_col_name or "win" == curr_col_name:
                    res_obj_win[curr_col_name] = curr_match_win[i]
                    res_obj_lose[curr_col_name] = curr_match_lose[i]
                # delta fields
                else:
                    res_obj_win[curr_col_name + "_delta"] = curr_match_win[i] - curr_match_lose[i]
                    res_obj_lose[curr_col_name + "_delta"] = -res_obj_win[curr_col_name + "_delta"]
            # add to response
            team_deltas_data.append(res_obj_win)
            team_deltas_data.append(res_obj_lose)
            # reset curr vars
            curr_match_id = row[0]
        if row[2] == "Win":
            curr_match_win = row
        else:
            curr_match_lose = row

    # finish populating last match
    res_obj_win = {}
    res_obj_lose = {}
    # process previous match
    for i in range(len(curr_match_win)):
        curr_col_name = column_names[i]
        # non-delta fields
        if "match_id" == curr_col_name or "team_id" == curr_col_name or "win" == curr_col_name:
            res_obj_win[curr_col_name] = curr_match_win[i]
            res_obj_lose[curr_col_name] = curr_match_lose[i]
        # delta fields
        else:
            res_obj_win[curr_col_name + "_delta"] = curr_match_win[i] - curr_match_lose[i]
            res_obj_lose[curr_col_name + "_delta"] = -res_obj_win[curr_col_name + "_delta"]
    # add to response
    team_deltas_data.append(res_obj_win)
    team_deltas_data.append(res_obj_lose)

    res["data"] = team_deltas_data

    return jsonify(res)
