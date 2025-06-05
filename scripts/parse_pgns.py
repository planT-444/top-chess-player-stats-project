from pathlib import Path
import json
import chess.pgn


root_dir = Path(__file__).parent.parent
player_ratings_filepath = root_dir / "output-files" / "player_ratings.json"
with open(player_ratings_filepath, 'r') as f:
    player_ratings = json.load(f)

# games -> player_name -> time_control -> games plus other data about them
games = {
    player_name: {
        "games": {
            "white": [],
            "black": []
        }
    } for player_name in player_ratings
}

pgns_dir = root_dir / "output-files" / "twic-pgns"

def parse_pgn(pgnpath) -> None:
    with open(pgnpath, encoding="utf-8") as pgn_file:
        while (game := chess.pgn.read_game(pgn_file)) is not None:
            white_player = game.headers.get("White", "")
            black_player = game.headers.get("Black", "")
            if white_player in games:
                games[white_player]["games"]["white"].append(str(game))
                print(white_player)
            if black_player in games:
                games[black_player]["games"]["black"].append(str(game))
                print(black_player)

file_count = 0
for pgnpath in pgns_dir.iterdir():
    print(f"Parsing:\n{pgnpath}\n")
    parse_pgn(pgns_dir / pgnpath)
    file_count += 1
    if file_count == 52:
        break

player_games_filepath = root_dir / "output-files" / "player_games.json"
with open(player_games_filepath, 'w') as f:
    json.dump(games, f, indent=4)

for player_name in games:
    white_games = games[player_name]["games"]["white"]
    black_games = games[player_name]["games"]["black"]
    print(f"{player_name}\n\tGame count: {len(white_games) + len(black_games)}\n")

