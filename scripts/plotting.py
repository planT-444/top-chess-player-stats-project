import json
import pprint
import statistics
from pathlib import Path
import matplotlib.pyplot as plt

def get_dataset(data_type, sub_type=None, outliers=()):
    return [
        all_player_data[player_name][data_type] 
            if sub_type is None
            else all_player_data[player_name][data_type][sub_type]
        for player_name in all_player_data 
            if player_name not in outliers
    ]

def scatterplot(
        filename, 
        title, 
        axis_dep, 
        axis_indep, 
        data_type_dep,
        data_type_indep,
        sub_type_dep=None,
        sub_type_indep=None,
        outliers=[],
        fig_num=None):
    fig, plot = plt.subplots()
    dep_dataset = get_dataset(data_type_dep, sub_type_dep, outliers)
    indep_dataset = get_dataset(data_type_indep, sub_type_indep, outliers)
    lin_regg = statistics.linear_regression(indep_dataset, dep_dataset)

    plot.set_title(title)
    plot.axline(
        xy1 = (0, lin_regg.intercept), 
        slope = lin_regg.slope, 
        label = f"r = {statistics.correlation(indep_dataset, dep_dataset)}"
    )
    plot.scatter(indep_dataset, dep_dataset)
    plot.set_xlabel(axis_indep)
    plot.set_ylabel(axis_dep)
    plot.legend()
    fig.savefig(graphs_dir / f"{filename}.png")


def boxplot(filename, title, labels, data_types, sub_types=None, tick_size=None, fig_num=None):
    fig, plot = plt.subplots()
    fig.set_figheight(1.5 + 0.5 * len(data_types))
    plt.subplots_adjust(bottom=0.25)
    if fig_num is not None:
        print("yeet")
        plot.text(0.5, -0.30, f"Figure {fig_num}", ha="center", color="black", fontsize=10, transform=plot.transAxes)

    sub_type = [None] * len(data_types) if sub_types is None else sub_types
    datasets = [get_dataset(data_types[i], sub_type[i]) for i in range(len(data_types))]
    plot.boxplot(datasets, vert=False, patch_artist=True, widths=0.5)
    plot.set_yticklabels(labels)
    plot.set_title(title)
    plot.grid(True)
    
    if tick_size is not None and isinstance(tick_size, int):
        tick_start = (
            min(min(dataset) for dataset in datasets) // tick_size) * tick_size      
        tick_end = ((max(max(dataset for dataset in datasets)) // tick_size) + 1) * tick_size
        plot.set_xticks(range(tick_start, tick_end + 1, tick_size))
        minor_tick_size = tick_size // 4
        plot.set_xticks(range(tick_start, tick_end + 1, minor_tick_size), minor=True)
        plot.grid(which='minor', color='gray', linestyle='--', linewidth=0.5)
    fig.savefig(graphs_dir / f"{filename}.png")



root_dir = Path(__file__).parent.parent
graphs_dir = root_dir / "output-files" / "graphs"
player_data_filepath = root_dir / "output-files" / "player_data.json"
player_ratings_filepath = root_dir / "output-files" / "player_ratings.json"
with open(player_data_filepath, 'r') as f:
    all_player_data = json.load(f)
with open(player_ratings_filepath, 'r') as f:
    for player_name, rating in json.load(f).items():
        all_player_data[player_name]["rating"] = rating

print(all_player_data['Carlsen,M'].keys())

# scatterplot(
#     "test2",
#     "Rating vs. Win rate",
#     "Rating (Classical + Rapid + Blitz)",
#     "Win rate",
#     "rating",
#     "win_rate",
#     sub_type_indep="all"
# )

# scatterplot(
#     "test2",
#     "Rating vs. draw rate",
#     "Rating (Classical + Rapid + Blitz)",
#     "draw rate",
#     "rating",
#     "draw_rate",
#     sub_type_indep="all"
# )

# scatterplot(
#     "test2",
#     "e",
#     "win rate",
#     "average move count",
#     "win_rate",
#     "avg_moves",
#     sub_type_dep="all",
#     sub_type_indep="all"
# )

boxplot("ratings_boxplot", "Top 20 Players' Ratings", [""], ["rating"], tick_size=100, fig_num=1)
boxplot("moves_boxplot", "Average Moves Per Game", ["draw", "loss", "win", "all"], ["avg_moves"] * 4, ["draw", "loss", "win", "all"], fig_num=2.1)
scatterplot(
    "rating_vs_draw_rate",
    "Rating vs. Draw rate",
    "Rating (Classical + Rapid + Blitz)",
    "Draw rate",
    "rating",
    "draw_rate",

    sub_type_indep="all"
)
scatterplot(
    "win_rate_vs_avg_moves_draw",
    "Win rate vs. Average moves to draw",
    "Win rate",
    "Avg moves to draw",
    "win_rate",
    "avg_moves",
    sub_type_dep="all",
    sub_type_indep="draw",
)

boxplot("avg_rating_diff", "Average Rating Difference", [""], ["avg_rating_diff"], ["all"], fig_num=2.2)