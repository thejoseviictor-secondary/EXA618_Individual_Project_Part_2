from flask import Flask, request, jsonify
from http import HTTPStatus
from dotenv import load_dotenv
from utils.parsers import collect_steam_games_data, collect_steam_game_dlcs_data
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
    collect_steam_games_data()

    games, err = get_games_data_in_database()
    if games or not err:
        return jsonify(games)
    else:
        print(err, flush=True)
        return jsonify({"error": "Erro interno ao buscar jogos!"}), HTTPStatus.INTERNAL_SERVER_ERROR

# Route to get game DLCs data on database, ordered by price:
@app.route('/get_game_dlcs_ordered_by_price/<game_id>', methods=['GET'])
def get_game_dlcs_ordered_by_price(game_id):
    collect_steam_game_dlcs_data(game_id)
    
    game_dlcs_data, err = get_game_dlcs_data_in_database_ordered_by_price(game_id)
    if game_dlcs_data or not err:
        return jsonify(game_dlcs_data)
    else:
        print(err, flush=True)
        return jsonify({"error": "Erro interno ao buscar DLCs deste jogo!"}), HTTPStatus.INTERNAL_SERVER_ERROR

# Route to get game DLCs data on database, ordered by release date:
@app.route('/get_game_dlcs_ordered_by_release_date/<game_id>', methods=['GET'])
def get_game_dlcs_ordered_by_release_date(game_id):
    collect_steam_game_dlcs_data(game_id)

    game_dlcs_data, err = get_game_dlcs_data_in_database_ordered_by_release_date(game_id)
    if game_dlcs_data or not err:
        return jsonify(game_dlcs_data)
    else:
        print(err, flush=True)
        return jsonify({"error": "Erro interno ao buscar DLCs deste jogo!"}), HTTPStatus.INTERNAL_SERVER_ERROR

if __name__ == '__main__':
    app.run(host=os.getenv("BACKEND_HOST"), port=os.getenv("BACKEND_PORT"), debug=True)
