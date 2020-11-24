from flask import Flask, jsonify
import os
import sqlite3

# set up flask
app = Flask(__name__)


@app.route('/match-history')
def get_match_hisotry():
    
    # connect to database
    db_name = "C:/Users/Ivan/Coding/sqlite/league.db"
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    sql = "SELECT * FROM Match LIMIT 10"
    c.execute(sql)

    rows = c.fetchall()

    return jsonify(rows)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)