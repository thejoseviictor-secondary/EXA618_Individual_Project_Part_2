from repository.db import get_connection
import mysql

# Function to check if the game is already in the database:
def is_game_in_database(game_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT game_id
            FROM steam_game_dlcs_schema.games
            WHERE game_id = (%s)
        """

        cursor.execute(sql, (game_id,))
        found_game = cursor.fetchall()

        cursor.close()
        conn.close()

        if found_game != []:
            return True, None
        else:
            return False, None
    except mysql.connector.Error as err:
        return False, err

# Function to get games data from database:
def get_games_data_in_database():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT * 
            FROM steam_game_dlcs_schema.games
        """

        cursor.execute(sql)
        games = cursor.fetchall()

        cursor.close()
        conn.close()

        return games, None
    except mysql.connector.Error as err:
        return False, err

# Function to insert a new game data in the database:
def insert_game_in_database(game_id, game_url, game_name, game_cover):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO steam_game_dlcs_schema.games (game_id, game_url, game_name, game_cover) 
            VALUES (%s, %s, %s, %s)
        """
        values = (int(game_id), str(game_url), str(game_name), str(game_cover))

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()

        return True, None
    except mysql.connector.Error as err:
        return False, err
    
# Function to update game data in the database:
def update_game_in_database(game_id, game_url, game_name, game_cover):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            UPDATE steam_game_dlcs_schema.games 
            SET game_url = %s, game_name = %s, game_cover = %s 
            WHERE game_id = %s
        """
        values = (int(game_id), str(game_url), str(game_name), str(game_cover), int(game_id))

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()

        return True, None
    except mysql.connector.Error as err:
        return False, err
