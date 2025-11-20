from flask import Flask, request, jsonify, render_template
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date
import requests


app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")

player_df = pd.read_csv("data/player_index.csv")

def get_latest_season():
    today = date.today()
    return today.year if today.month >= 10 else today.year - 1

import unicodedata
import re

def normalize(s):
    if not isinstance(s, str):
        return ""
    s = s.lower().strip()
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9\s]", "", s)  # remove *, accents, punctuation
    return s

def find_player_suffix(name):
    target = normalize(name)

    if "clean_name" not in player_df.columns:
        player_df["clean_name"] = player_df["player_name"].apply(normalize)

    row = player_df[player_df["clean_name"] == target]
    if len(row) > 0:
        return row.iloc[0]["suffix"]

    row = player_df[player_df["clean_name"].str.contains(target)]
    if len(row) > 0:
        return row.iloc[0]["suffix"]

    last = target.split()[-1]
    row = player_df[player_df["clean_name"].str.endswith(" " + last)]
    if len(row) > 0:
        return row.iloc[0]["suffix"]

    return None


def get_game_log_table(suffix, season):
    url = f"https://www.basketball-reference.com/players/{suffix[0]}/{suffix}/gamelog/{season}/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    }

    try:
        html = requests.get(url, headers=headers).text

        tables = pd.read_html(html)
        
        for table in tables:
            if "PTS" in table.columns and "TRB" in table.columns and "AST" in table.columns:
                return table
    except Exception as e:
        print("Error:", e)
        return None

    return None


@app.get("/player")
def get_player():
    name = request.args.get("name")
    season = request.args.get("season")

    if not name:
        return jsonify({"error": "Missing name!"}), 400

    if not season:
        season = get_latest_season()

    try:
        season = int(season)
    except:
        return jsonify({"error": "Season must be an integer!"}), 400

    suffix = find_player_suffix(name)
    if suffix is None:
        return jsonify({"error": "Player not found!"}), 404

    df = get_game_log_table(suffix, season)
    if df is None:
        return jsonify({"error": "Game logs not found"}), 404

    return df.to_json(orient="records")


if __name__ == "__main__":
    app.run(debug=True)