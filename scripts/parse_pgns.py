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
        time_control: 
            {'games': []}
        for time_control in ("blitz", "rapid", "classical")
    } for player_name in player_ratings
}

print(games)

def parse_pgn(filepath):
    pass