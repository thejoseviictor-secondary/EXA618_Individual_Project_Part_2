from flask import Flask, request, jsonify
from http import HTTPStatus
from dotenv import load_dotenv
from utils.data_update import is_dlc_data_more_than_one_day_old, update_games_data_async, update_dlcs_data_async
from repository.games_repository import get_games_data_in_database
from repository.dlcs_repository import get_game_dlcs_data_in_database_ordered_by_price
from repository.dlcs_repository import get_game_dlcs_data_in_database_ordered_by_release_date
import os

# Loading environment variables:
load_dotenv()

app = Flask(__name__)

# Route to get games from Steam and database:
@app.route('/get_games', methods=['GET'])
def get_games():
    games, err = get_games_data_in_database()
    if games or not err:
        return jsonify(games)
    else:
        print(err, flush=True)
        return jsonify({"error": "Erro interno ao buscar jogos!"}), HTTPStatus.INTERNAL_SERVER_ERROR

# Route to get game DLCs data on database, ordered by price:
@app.route('/get_game_dlcs_ordered_by_price/<game_id>', methods=['GET'])
def get_game_dlcs_ordered_by_price(game_id):    
    game_dlcs_data, err = get_game_dlcs_data_in_database_ordered_by_price(game_id)
    if game_dlcs_data or not err:
        dlc_access_date = game_dlcs_data[0]["dlc_access_date"]
        print(dlc_access_date, flush=True)
        if is_dlc_data_more_than_one_day_old(dlc_access_date):
            update_games_data_async()
            update_dlcs_data_async(game_id)
        
        return jsonify(game_dlcs_data)
    else:
        print(err, flush=True)
        return jsonify({"error": "Erro interno ao buscar DLCs deste jogo!"}), HTTPStatus.INTERNAL_SERVER_ERROR

# Route to get game DLCs data on database, ordered by release date:
@app.route('/get_game_dlcs_ordered_by_release_date/<game_id>', methods=['GET'])
def get_game_dlcs_ordered_by_release_date(game_id):
    game_dlcs_data, err = get_game_dlcs_data_in_database_ordered_by_release_date(game_id)
    if game_dlcs_data or not err:
        dlc_access_date = game_dlcs_data[0]["dlc_access_date"]
        if is_dlc_data_more_than_one_day_old(dlc_access_date):
            update_games_data_async()
            update_dlcs_data_async(game_id)
        
        return jsonify(game_dlcs_data)
    else:
        print(err, flush=True)
        return jsonify({"error": "Erro interno ao buscar DLCs deste jogo!"}), HTTPStatus.INTERNAL_SERVER_ERROR

if __name__ == '__main__':
    app.run(host=os.getenv("BACKEND_HOST"), port=os.getenv("BACKEND_PORT"), debug=True)
