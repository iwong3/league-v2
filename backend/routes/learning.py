from flask import Blueprint, jsonify, request
from flask_cors import CORS

import json
import os
import random
import sqlite3
import sys
import time

from utility import constants, map_util, sqlite_util


# flask setup
learning_bp = Blueprint("learning", __name__)

# constants
DEFAULT_ROW_LIMIT = 1
DEFAULT_MAP_ID = 11


def get_blueprint():
    return learning_bp

@learning_bp.route('/learning/team-win-prediction', methods=['GET'])
def get_team_win_prediction():

    print("/learning/team-win-predicton endpoint hit")

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
        "SELECT m.id, mp.champion_id, mp.spell_1_id, mp.spell_2_id, "
        "mp.perk_0, mp.perk_1, mp.perk_2, mp.perk_3, mp.perk_4, mp.perk_5, "
        "mp.stat_perk_0, mp.stat_perk_1, mp.stat_perk_2, mp.win "
        "FROM {} AS m "
        "INNER JOIN {} AS mp "
        "ON m.id = mp.match_id "
        "WHERE m.id IN "
        "(SELECT id FROM {} ORDER BY RANDOM() LIMIT {}) "
        "AND m.map_id = {}"
    ).format(constants.MATCH_TABLE_NAME, constants.MATCH_PARTICIPANTS_TABLE_NAME, constants.MATCH_TABLE_NAME, limit, map_id)
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
    attributes = []
    labels = []
    curr_attributes = []
    curr_match_id = rows[0][0]
    curr_win_data = []
    curr_lose_data = []

    # populate learning data
    for row in rows:
        # new match - process previous match data and reset curr vars
        if curr_match_id != row[0]:
            # process win
            while len(curr_win_data) > 0:
                curr_participant = random.sample(curr_win_data, 1)[0]
                for i in range(len(curr_participant)):
                    curr_attributes.append(curr_participant[i])
                curr_win_data.remove(curr_participant)
            attributes.append(curr_attributes)
            labels.append(1)
            # process loss
            while len(curr_lose_data) > 0:
                curr_participant = random.sample(curr_lose_data, 1)[0]
                for i in range(len(curr_participant)):
                    curr_attributes.append(curr_participant[i])
                curr_lose_data.remove(curr_participant)
            attributes.append(curr_attributes)
            labels.append(0)
            # reset curr vars
            curr_attributes = []
            curr_match_id = row[0]
        # record curr match participant
        if row[-1] == 1:
            curr_win_data.append(row)
        else:
            curr_lose_data.append(row)

    # finish populating last match
    # process win
    while len(curr_win_data) > 0:
        curr_participant = random.sample(curr_win_data, 1)[0]
        for i in range(len(curr_participant)):
            curr_attributes.append(curr_participant[i])
        curr_win_data.remove(curr_participant)
    attributes.append(curr_attributes)
    labels.append(1)
    # process loss
    while len(curr_lose_data) > 0:
        curr_participant = random.sample(curr_lose_data, 1)[0]
        for i in range(len(curr_participant)):
            curr_attributes.append(curr_participant[i])
        curr_lose_data.remove(curr_participant)
    attributes.append(curr_attributes)
    labels.append(0)

    # finalize training data
    training_data.append(attributes)
    training_data.append(labels)

    print(training_data)

    # send training data to random forest

    return jsonify([])
