from dotenv import load_dotenv
from ratelimit import limits, sleep_and_retry

import os
import requests
import sqlite3


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
RATE_LIMIT_CALLS = 45
RATE_LIMIT_DURATION = 120 # 2 minutes

count = 1

# FLOW
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

    test_results = []

    # account ids and match ids to query
    account_ids = []
    match_ids = []

    # get initial account id
    summoner_request_url = NA_ENDPOINT + SUMMONER_BY_NAME_PATH + summoner_name
    summoner_response_data = call_api(summoner_request_url, request_headers).json()

    account_id = summoner_response_data["accountId"]
    account_ids.append(account_id)

    # for all account ids
    while len(account_ids) > 0:
        
        # get matchlist
        account_id = account_ids.pop()
        matchlist_request_url = NA_ENDPOINT + MATCHLIST_BY_ACCOUNT_PATH + account_id
        matchlist_response_data = call_api(matchlist_request_url, request_headers).json()

        # add all match ids from matchlist
        for match in matchlist_response_data["matches"]:
            match_id = match["gameId"]
            match_ids.append(match_id)
        
        # for all match ids
        while len(match_ids) > 0:
            
            # get match
            match_id = match_ids.pop()
            match_request_url = NA_ENDPOINT + MATCH_BY_ID_PATH + str(match_id)
            match_response_data = call_api(match_request_url, request_headers).json()

            test_results.append(match_response_data["gameId"])

            # add participant account ids

            # insert match data into db
    
    print(test_results)


@sleep_and_retry
@limits(calls=RATE_LIMIT_CALLS, period=RATE_LIMIT_DURATION)
def call_api(url, headers):

    global count

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(url, "failed with", response.status_code)
    
    print("Call",count)
    count += 1
    
    return response


if __name__ == "__main__":
    get_matches("Jhun")
