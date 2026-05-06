from datetime import datetime, timedelta, timezone
from threading import Thread
from utils.parsers import collect_steam_games_data, collect_steam_game_dlcs_data

updating_games_data = False
updating_games_dlcs = set()

# Checking if the DLC data in the database is more than 1 day old:
def is_dlc_data_more_than_one_day_old(last_access_date):
    if not last_access_date:
        return True
    
    print(datetime.now(timezone.utc), flush=True)
    print(last_access_date, flush=True)
    return datetime.now(timezone.utc) - last_access_date > timedelta(days=1)

def update_games_data_async():
    global updating_games_data

    if updating_games_data:
        return
    
    updating_games_data = True
    
    def task():
        global updating_games_data

        try:
            collect_steam_games_data()
        finally:
            updating_games_data = False

    thread = Thread(target=task)
    thread.daemon = True
    thread.start()

def update_dlcs_data_async(game_id):
    if game_id in updating_games_dlcs:
        return
    
    updating_games_dlcs.add(game_id)

    def task():
        try:
            collect_steam_game_dlcs_data(game_id)
        finally:
            updating_games_dlcs.discard(game_id)
    
    thread = Thread(target=task)
    thread.daemon = True
    thread.start()
