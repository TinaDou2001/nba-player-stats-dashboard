import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_all_player_suffixes():
    all_players = []

    for last_name_letter in "abcdefghijklmnopqrstuvwxyz":
        index_url = f"https://www.basketball-reference.com/players/{last_name_letter}/"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(index_url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        for row in soup.select("table tbody tr"):
            th = row.find("th", {"data-stat": "player"})
            if th:
                name = th.text.strip()
                suffix = th["data-append-csv"]
                all_players.append((name, suffix))

    df = pd.DataFrame(all_players, columns=["player_name", "suffix"])
    df.to_csv("data/player_index.csv", index=False)


if __name__ == "__main__":
    get_all_player_suffixes()