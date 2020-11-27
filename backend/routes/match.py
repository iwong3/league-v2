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


def get_blueprint():
    return match_bp

@match_bp.route('/match', methods=['GET'])
def get_match():

    print("/match endpoint hit")

    # read request args
    limit = request.args.get("limit", DEFAULT_ROW_LIMIT)

    # connect to database
    db_name = "C:/Users/Ivan/Coding/sqlite/league.db"
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # get query results
    sql = (
        "SELECT * FROM {} AS m "
        "INNER JOIN {} AS mp "
        "ON m.id = mp.match_id "
        "ORDER BY RANDOM() "
        "LIMIT {}"
    ).format(constants.MATCH_TABLE_NAME, constants.MATCH_PARTICIPANTS_TABLE_NAME, limit)
    cursor.execute(sql)
    rows = cursor.fetchall()

    # set up response
    res = []
    column_names = sqlite_util.get_column_names(cursor)

    # create response object for each row and add to response
    for row in rows:
        res_obj = {}
        # add each column to response object
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
        res.append(res_obj)

    return jsonify(res)
