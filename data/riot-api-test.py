import requests
import sqlite3

# TODO
# - set keys in env vars
# - gitignore for secure things, packages
# - make sure script is idempotent, wont add dup rows

# connect to database
db_name = "C:/Users/Ivan/Coding/sqlite/league.db"
conn = sqlite3.connect(db_name)
c = conn.cursor()

# set up riot api endpoint
riot_api_key = "RGAPI-4ba0548f-5ca9-4652-88fc-9c720765c4ce" # temp key - will expire
na_endpoint = "https://na1.api.riotgames.com"
match_endpoint = "/lol/match/v4/matchlists/by-account/"

summoner_data = {
    "id": "aNlE3brG6pECUas7AnbZSklUPmAPAc9C5M6f7BGvHjKyID0",
    "accountId": "UMcRDiI-gqxc7okDz6SnY_jDUy2XCI1gtQaFM330-QAQ3g",
    "puuid": "uVqt0hVSYw5BOw5oFRmPyWKhFWM8mi2Bo70Q-DEMprEXCIzVPy1Iov7lj88eq_EN1IFO9Co-RALMug",
    "name": "Jhun",
    "profileIconId": 3152,
    "revisionDate": 1606046943000,
    "summonerLevel": 197
}

request_url = na_endpoint + match_endpoint + summoner_data["accountId"]
request_headers = { "X-Riot-Token": riot_api_key }

# make the call
response_data = requests.get(request_url, headers=request_headers).json()

# load data into sqlite
for match in response_data["matches"]:

    id = match["gameId"]
    champion = match["champion"]
    queue = match["queue"]
    season = match["season"]
    timestamp = match["timestamp"]

    sql = "INSERT INTO Match VALUES (?, ?, ?, ?, ?)"
    c.execute(sql, (id, champion, queue, season, timestamp))

# commit and close db connection
conn.commit()
conn.close()