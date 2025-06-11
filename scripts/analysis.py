from pathlib import Path
from io import StringIO
import json
import chess.pgn
from statistics import stdev
import pprint

root_dir = Path(__file__).parent.parent
games_filepath = root_dir / "output-files" / "player_games.json"
output_filepath = root_dir / "output-files" / "player_data.json"
with open(games_filepath, 'r') as f:
    all_player_data = json.load(f)

# for player_name in games:
#     white_games = games[player_name]["games"]["white"]
#     black_games = games[player_name]["games"]["black"]
#     print(f"{player_name}\n\tGame count: {len(white_games) + len(black_games)}\n")



# (for testing)
# if True:
#     player_name = "Nepomniachtchi,I"
for player_name in all_player_data:
    player_data = all_player_data[player_name]
    player_data["game_counts"] = {k: 0 for k in ("white", "black", "win", "loss", "draw", "all")}
    player_data["win_rate"] = {k: 0 for k in ("white", "black", "all")}
    player_data["draw_rate"] = {k: 0 for k in ("white", "black", "all")}
    player_data["avg_moves"] = {k: 0 for k in ("win", "loss", "draw", "all")}
    player_data["avg_rating_diff"] = {k: 0 for k in ("win", "loss", "draw", "all")}
    player_data["games_per_month"] = {}
    player_data["win_rate_per_month"] = {}
    player_games = player_data["games"]
    for color in ("white", "black"):
        for i, game in enumerate(player_games[color]):
            game = chess.pgn.read_game(StringIO(game))
            if game is None or game.headers.get("Variant", None) is not None:
                continue
            
            move_count = sum(1 for _ in game.mainline_moves()) / 2
            encoded_result = game.headers["Result"]
            win_result = "1-0" if color == "white" else "0-1"
            try:
                rating_diff = (1 if color == "white" else -1) * \
                    (int(game.headers["WhiteElo"]) - int(game.headers["BlackElo"]))
            except:
                print(game.headers)
                continue
            
            month = game.headers["Date"][:7]
            
            if month not in player_data["games_per_month"]:
                player_data["games_per_month"][month] = 0
                player_data["win_rate_per_month"][month] = 0
            player_data["games_per_month"][month] += 1
            

            if encoded_result == win_result:
                decoded_result = "win"
                player_data["win_rate"][color] += 1
                player_data["win_rate"]["all"] += 1
                player_data["win_rate_per_month"][month] += 1
            elif encoded_result == "1/2-1/2":
                decoded_result = "draw"
                player_data["draw_rate"][color] += 1
                player_data["draw_rate"]["all"] += 1
            else:
                decoded_result = "loss"

            player_data["game_counts"][color] += 1

            player_data["game_counts"][decoded_result] += 1
            player_data["avg_moves"][decoded_result] += move_count
            player_data["avg_rating_diff"][decoded_result] += rating_diff

            player_data["game_counts"]["all"] += 1
            player_data["avg_moves"]["all"] += move_count
            player_data["avg_rating_diff"]["all"] += rating_diff

            
    for data_type in ("win_rate", "draw_rate", "avg_moves", "avg_rating_diff"):
        player_data[data_type] = {
            k: v / player_data["game_counts"][k] for k, v in player_data[data_type].items()
        }
    player_data["win_rate_per_month"] = {
            month: wins / player_data["games_per_month"][month] 
                for month, wins in player_data["win_rate_per_month"].items()
    }
    player_data["win_rate_stdev"] = stdev(player_data["win_rate_per_month"].values())

all_player_data_without_games = all_player_data.copy()
for player_name in all_player_data_without_games:
    del all_player_data_without_games[player_name]["games"]
pprint.pp(all_player_data_without_games)

with open(output_filepath, 'w') as f:
    json.dump(all_player_data_without_games, f, indent=4)