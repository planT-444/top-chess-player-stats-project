import json
import pprint
import statistics
from pathlib import Path
import matplotlib.pyplot as plt

def get_dataset(data_type, sub_type=None, outlier_names=[]):
    return [
        all_player_data[player_name][data_type] 
            if sub_type is None
            else all_player_data[player_name][data_type][sub_type]
        for player_name in all_player_data 
            if player_name not in outlier_names
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
        outliers=[]):
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

win_rate_stdev = [v["win_rate_stdev"] for v in all_player_data.values()]
rating = [v["rating"] for v in all_player_data.values()]
avg_moves = [v["avg_moves"] for v in all_player_data.values()]



# rating_vs_wrate_stdev
rating_vs_wrate_stdev, plot = plt.subplots()
lin_regg = statistics.linear_regression(win_rate_stdev, rating)
plot.set_title("Rating vs. Std dev. of monthly win rate")
plot.axline(xy1 = (0, lin_regg.intercept), slope = lin_regg.slope, label = f"r = {statistics.correlation(win_rate_stdev, rating)}")
plot.scatter(win_rate_stdev, rating)
plot.set_xlabel("Std deviation of monthly win rate")
plot.set_ylabel("Rating (Classical + Rapid + Blitz)")
plot.legend()
rating_vs_wrate_stdev.savefig(graphs_dir / "rating_vs_wrate_stdev_woutlier.png")


# rating_vs_wrate_stdev without outlier
rating_vs_wrate_stdev, plot = plt.subplots()
outliers = ("Carlsen,M", "Andreikin,D")
adjusted_win_rate_stdev = get_dataset("win_rate_stdev", outliers)
adjusted_rating = get_dataset("rating", outliers)
lin_regg = statistics.linear_regression(
    adjusted_win_rate_stdev,
    adjusted_rating 
)

plot.set_title("Rating vs. Std dev. of monthly win rate (without Carlsen, Andreikin)")
plot.axline(xy1 = (0, lin_regg.intercept), slope = lin_regg.slope, label = f"r = {statistics.correlation(adjusted_win_rate_stdev,
    adjusted_rating )}")
plot.scatter(adjusted_win_rate_stdev, adjusted_rating)
plot.set_xlabel("Std deviation of monthly win rate")
plot.set_ylabel("Rating (Classical + Rapid + Blitz)")
plot.legend()
rating_vs_wrate_stdev.savefig(graphs_dir / "rating_vs_wrate_stdev_wooutlier.png")

plt.show()


scatterplot(
    "test",
    "Rating vs. Std dev of monthly win rate",
    "Rating (Classical + Rapid + Blitz)",
    "Std deviation of monthly win rate",
    "rating",
    "win_rate_stdev"
)