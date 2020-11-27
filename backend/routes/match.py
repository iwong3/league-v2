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
DEFAULT_ROW_LIMIT = 100


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
            if "champion_id" == column_names[i]:
                res_obj[column_names[i]] = map_util.get_champion_name(row[i])
            else:
                res_obj[column_names[i]] = row[i]
        res.append(res_obj)

    return jsonify(res)
