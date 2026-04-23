from repository.db import get_connection
import mysql

# Function to check if the game DLC is already in the database:
def is_game_dlc_in_database(dlc_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT dlc_id 
            FROM steam_game_dlcs_schema.dlcs 
            WHERE dlc_id = (%s)
        """

        cursor.execute(sql, (dlc_id,))
        found_game_dlc = cursor.fetchall()

        cursor.close()
        conn.close()

        if found_game_dlc != []:
            return True, None
        else:
            return False, None
    except mysql.connector.Error as err:
        return False, err

# Function to get the game DLCs data from database, ordered by price:
def get_game_dlcs_data_in_database_ordered_by_price(game_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT * 
            FROM steam_game_dlcs_schema.dlcs 
            WHERE dlc_game_id = (%s) 
            ORDER BY dlc_actual_price ASC
        """

        cursor.execute(sql, (game_id,))
        game_dlcs = cursor.fetchall()

        cursor.close()
        conn.close()

        return game_dlcs, None
    except mysql.connector.Error as err:
        return None, err

# Function to get the game DLCs data from database, ordered by release_date:
def get_game_dlcs_data_in_database_ordered_by_release_date(game_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT * 
            FROM steam_game_dlcs_schema.dlcs 
            WHERE dlc_game_id = (%s) 
            ORDER BY dlc_release_date ASC
        """

        cursor.execute(sql, (game_id,))
        game_dlcs = cursor.fetchall()

        cursor.close()
        conn.close()

        return game_dlcs, None
    except mysql.connector.Error as err:
        return None, err

# Function to insert a new game DLC data in the database:
def insert_game_dlc_in_database(dlc_id, dlc_url, dlc_name, dlc_cover, dlc_release_date, dlc_actual_price, dlc_access_date, dlc_game_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO steam_game_dlcs_schema.dlcs
                (dlc_id, dlc_url, dlc_name, dlc_cover, dlc_release_date, dlc_actual_price, dlc_access_date, dlc_game_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            int(dlc_id), str(dlc_url), str(dlc_name), 
            str(dlc_cover), dlc_release_date, dlc_actual_price, 
            dlc_access_date, int(dlc_game_id)
        )

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()

        return True, None
    except mysql.connector.Error as err:
        print(err, flush=True)
        return False, err
    
# Function to update a game DLC data in the database:
def update_game_dlc_in_database(dlc_id, dlc_url, dlc_name, dlc_cover, dlc_release_date, dlc_actual_price, dlc_access_date, dlc_game_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            UPDATE steam_game_dlcs_schema.dlcs 
            SET dlc_url = %s, dlc_name = %s, dlc_cover = %s, dlc_release_date = %s, 
                dlc_actual_price = %s, dlc_access_date = %s, dlc_game_id = %s
            WHERE dlc_id = %s
        """
        values = (
            int(dlc_id), str(dlc_url), str(dlc_name), 
            str(dlc_cover), dlc_release_date, dlc_actual_price, 
            dlc_access_date, int(dlc_game_id)
        )

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()

        return True, None
    except mysql.connector.Error as err:
        print(err, flush=True)
        return False, err
