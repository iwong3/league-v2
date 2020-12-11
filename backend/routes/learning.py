from flask import Blueprint, jsonify, request
from flask_cors import CORS
from math import floor

import json
import os
import random
import sqlite3
import sys
import time

from utility import constants, map_util, sqlite_util
from backend.process import random_forests


# flask setup
learning_bp = Blueprint("learning", __name__)

# constants
DEFAULT_ROW_LIMIT = 1
DEFAULT_MAP_ID = 11


def get_blueprint():
    return learning_bp

@learning_bp.route('/learning/champ-prediction', methods=['GET'])
def get_champ_prediction():

    print("/learning/champ-predicton endpoint hit")

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
    sql2 = (
        "SELECT * FROM Match LIMIT {}"
    ).format(limit)
    sql = (
        "SELECT m.id, m.game_duration, mp.champion_id, "
        "mp.kills, mp.deaths, mp.assists, mp.total_minions_killed, "
        "mp.physical_damage_dealt, mp.magic_damage_dealt, mp.true_damage_dealt, mp.total_damage_dealt, "
        "mp.physical_damage_dealt_to_champions, mp.magic_damage_dealt_to_champions, "
        "mp.true_damage_dealt_to_champions, mp.total_damage_dealt_to_champions, mp.largest_critical_strike, "
        "mp.physical_damage_taken, mp.magic_damage_taken, mp.true_damage_taken, mp.total_damage_taken, "
        "mp.damage_self_mitigated, mp.total_heal, mp.total_units_healed, "
        "mp.neutral_minions_killed, mp.neutral_minions_killed_team_jungle, mp.neutral_minions_killed_enemy_jungle, "
        "mp.total_time_crowd_control_dealt, mp.time_ccing_others, "
        "mp.gold_earned, mp.gold_spent, mp.vision_score "
        "FROM {} AS m "
        "INNER JOIN {} AS mp "
        "ON m.id = mp.match_id "
        "WHERE m.map_id = {} "
        "ORDER BY RANDOM() "
        "LIMIT {}"
    ).format(constants.MATCH_TABLE_NAME, constants.MATCH_PARTICIPANTS_TABLE_NAME, map_id, limit)
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

    # set up training data
    training_data = []
    curr_data = []
    attributes = []
    labels = []

    # populate learning data
    for row in rows:
        curr_data = list(row[3:])
        curr_data.append(row[2])
        training_data.append(curr_data)

    # keep 10% of data for testing
    num_test = floor(int(limit) / 10)
    test_attrs = []
    test_labels = []
    while num_test > 0:
        test_data = training_data.pop()
        test_attrs.append(test_data[:-1])
        test_labels.append(test_data[-1])
        num_test -= 1

    # train random forest on training data
    num_trees = 20
    random_forest = random_forests.RandomForest(num_trees)
    random_forest.bootstrapping(training_data)
    random_forest.fitting()

    # predict on test data
    predicted_champs = random_forest.voting(test_attrs)

    # calculate accuracy and predictions for res
    res["predictions"] = []
    num_right = 0
    num_labels = len(test_labels)
    for i in range(num_labels):
        res["predictions"].append({
            "actual": test_labels[i],
            "prediction": predicted_champs[i]
        })
        if test_labels[i] == predicted_champs[i]:
            num_right += 1
    accuracy = float(num_right) / num_labels

    res["accuracy"] = accuracy

    return jsonify(res)
