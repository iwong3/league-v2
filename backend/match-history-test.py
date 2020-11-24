from flask import Flask, jsonify
from flask_cors import CORS

import json
import os
import sqlite3
import time


# set up flask
app = Flask(__name__)
CORS(app)

@app.route('/match-history')
def get_match_history():
    
    # champion map
    with open("champions.json", encoding="utf8") as file:
        champion_json = json.load(file)
        champion_data = champion_json["data"]

    # connect to database
    db_name = "C:/Users/Ivan/Coding/sqlite/league.db"
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # get query results
    sql = "SELECT * FROM Match LIMIT 10"
    c.execute(sql)
    rows = c.fetchall()

    # set up response
    res = []
    for row in rows:

        # get champion name
        champion_name = "n/a"
        champion_id = row[1]
        for champion in champion_data:
            if champion_data[champion]["key"] == str(champion_id):
                champion_name = champion_data[champion]["name"]
        
        # get date
        date = time.strftime('%b %d, %Y @ %H:%M %p', time.localtime(row[4] / 1000))

        # create response
        res.append({
            "champion_name": champion_name,
            "date": date
        })

    return jsonify(res)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)