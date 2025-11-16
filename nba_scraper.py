import requests
from bs4 import BeautifulSoup
import pandas as pd
import statistics
from datetime import date

# Step 1: Get player's Basketball Reference suffix
def get_player_suffix(player_name):
    # LeBron James will give you j
    last_name_letter = player_name.split()[-1][0].lower()
    index_url = f"https://www.basketball-reference.com/players/{last_name_letter}/"
    # This will be https://www.basketball-reference.com/players/j/
    headers = {"User-Agent": "Mozilla/5.0"}
    # Sends an HTTP GET request to the index_url
    # Stores the response (HTML page) in the variable res
    res = requests.get(index_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    for row in soup.select("table tbody tr"):
        name_cell = row.find("th", {"data-stat": "player"})
        if name_cell and player_name.lower() in name_cell.text.lower():
            suffix = name_cell["data-append-csv"]
            return suffix
    return None


# Step 2: Get current NBA season year (latest available)
def get_latest_season():
    today = date.today()
    return today.year if today.month >= 10 else today.year - 1

# Step 3: Get the stats table using pandas.read_html
def get_game_log_table(suffix, season):
    url = f"https://www.basketball-reference.com/players/{suffix[0]}/{suffix}/gamelog/{season}/"
    print(f"Fetching: {url}")
    try:
        tables = pd.read_html(url)
        for table in tables:
            if "PTS" in table.columns and "TRB" in table.columns and "AST" in table.columns:
                return table
    except Exception as e:
        print(f"Error reading tables: {e}")
    return None

# Step 4: Calculate medians
def calculate_medians(df):
    # Drop rows where 'Gcar' is not a number (e.g., "Inactive", "Did Not Dress", or duplicate headers)
    df_clean = df[pd.to_numeric(df["Gcar"], errors="coerce").notna()].copy()

    # Convert all numeric-looking columns to numeric
    for col in df_clean.columns:
        df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")

    # Only keep numeric columns
    numeric_cols = df_clean.select_dtypes(include="number").columns

    # Compute medians
    medians = df_clean[numeric_cols].median()
    return medians
