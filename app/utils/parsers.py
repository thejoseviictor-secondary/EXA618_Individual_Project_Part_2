from datetime import date, datetime
from bs4 import BeautifulSoup
from datetime import date, datetime
import urllib.request
from repository.games_repository import is_game_in_database, insert_game_in_database, update_game_in_database
from repository.dlcs_repository import is_game_dlc_in_database, insert_game_dlc_in_database, update_game_dlc_in_database

# Today's date (ISO 8601):
todays_date = date.today().isoformat()

# Root game page on "Steam":
steam_game_root_seed = "https://store.steampowered.com/app/"

# Root game DLCs page on "Steam":
steam_dlc_root_seed = "https://store.steampowered.com/dlc/"

# Example "https://store.steampowered.com/dlc/{game_id}":
games_id_collection = [
    270880, 227300, 883710, 952060, 2050650, 244210, 291550, 690790, 2357570, 1938090,
    418370, 582010, 1196590, 230410, 2300320, 252490, 359550, 239140, 1984270, 1222670
]

# Function to set price to float:
def parse_dlc_actual_price(price_str):
    if not price_str:
        return 0.0
    
    # Free DLCs:
    if "." not in price_str and "," not in price_str:
        return 0.0
    
    # Paid DLCs:
    price_str = price_str.replace("$", "").strip()

    try:
        return float(price_str)
    except:
        return 0.0

# Function to set release date to ISO 8601:
def parse_dlc_release_date(date_str):
    try:
        dt = datetime.strptime(date_str, "%d %b, %Y")
        return dt.strftime("%Y-%m-%d")
    except:
        return None

# Parser function to collect game data from "Steam":
def collect_steam_games_data():
    for game_id in games_id_collection:
        seed = steam_dlc_root_seed + str(game_id)

        req = urllib.request.Request(
            seed,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        page = urllib.request.urlopen(req)
        html = str(page.read().decode("utf-8"))

        soup = BeautifulSoup(html, "html.parser")

        # URL:
        game_url = steam_game_root_seed + str(game_id)

        # Game name:
        h2_tag = soup.find("h2", class_="pageheader curator_name")
        if h2_tag:
            a_tag = h2_tag.find("a")
            if a_tag:
                game_name = a_tag.get_text(strip=True)

        # Game cover:
        img_tag = soup.find("img", class_="curator_avatar")
        if img_tag:
            game_cover = img_tag.attrs.get("src")
        
        # Inserting/Updating the game data into the database:
        if game_id and game_url and game_name and game_cover:
            found_game, err = is_game_in_database(game_id)
            if found_game and not err:
                update_game_in_database(game_id, game_url, game_name, game_cover)
            else:
                insert_game_in_database(game_id, game_url, game_name, game_cover)

# Parser function to collect game DLCs data from "Steam":
def collect_steam_game_dlcs_data(game_id):
    seed = steam_dlc_root_seed + str(game_id)

    req = urllib.request.Request(
        seed,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    page = urllib.request.urlopen(req)
    html = str(page.read().decode("utf-8"))

    soup = BeautifulSoup(html, "html.parser")
    
    # Game DLCs data:
    for div in soup.find_all("div", class_="recommendation"):
        # Resetting variables:
        dlc_id = None
        dlc_url = None
        dlc_name = None
        dlc_cover = None
        dlc_release_date = None
        dlc_actual_price = None

        # ID:
        inner_a = div.find("a", class_="store_capsule price_inline")
        if inner_a:
            dlc_id = inner_a.attrs.get("data-ds-appid")

        # URL:
        dlc_url = steam_game_root_seed + str(dlc_id)

        # Cover:
        inner_div = div.find("div", class_="capsule capsule_image_ctn smallcapsule")
        if inner_div:
            img_tag = inner_div.find("img")
            if img_tag:
                dlc_cover = img_tag.attrs.get("src")

        # Actual price:
        inner_div = div.find("div", class_="discount_final_price")
        if inner_div:
            dlc_actual_price = parse_dlc_actual_price(inner_div.get_text(strip=True))
            print(f"Parsed price {dlc_actual_price}", flush=True)

        # Name:
        inner_span = div.find("span", class_="color_created")
        if inner_span:
            dlc_name = inner_span.get_text(strip=True)

        # Release date:
        inner_span = div.find("span", class_="curator_review_date")
        if inner_span:
            dlc_release_date = parse_dlc_release_date(inner_span.get_text(strip=True))

        # Inserting/Updating the game DLC data into the database:
        if dlc_id and dlc_url and dlc_name and dlc_cover and dlc_release_date:
            found_game_dlc, err = is_game_dlc_in_database(dlc_id)
            if found_game_dlc and not err:
                update_game_dlc_in_database(dlc_id, dlc_url, dlc_name, dlc_cover, dlc_release_date, dlc_actual_price, todays_date, game_id)
            else:
                insert_game_dlc_in_database(dlc_id, dlc_url, dlc_name, dlc_cover, dlc_release_date, dlc_actual_price, todays_date, game_id)
