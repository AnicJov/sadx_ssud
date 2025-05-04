import srcomapi, srcomapi.datatypes as srcdt
from pprint import pprint
import statistics as stats
import datetime as dt
import itertools
import matplotlib.pyplot as plt
import numpy as np


def main():
    # Setup SRC API
    srcapi = srcomapi.SpeedrunCom()
    srcapi.debug = 0

    # Find SADX main board
    games = srcapi.search(srcdt.Game, {"name": r"Sonic Adventure DX"})
    game = None

    for g in games:
        if g.name == "Sonic Adventure DX: Director's Cut":
            game = g

    print(game.name)

    # Get all categories
    sadx_runs = {}
    for category in game.categories:
        if not category.name in sadx_runs:
            sadx_runs[category.name] = {}
        if category.type == 'per-level':
            continue
        sadx_runs[category.name] = srcdt.Leaderboard(srcapi, data=srcapi.get("leaderboards/{}/category/{}?platform=8gej2n93&embed=variables".format(game.id, category.id)))

    # Remove unneeded categories
    small_stories = ["Tails' Story", "Knuckles' Story", "Amy's Story", "Big's Story", "Gamma's Story", "Super Sonic's Story"]
    categories = {}
    for k, v in sadx_runs.items():
        if k in small_stories:
            categories[k] = v

    # Get statistics
    category_stats = {}
    for cat in small_stories:
        category_stats[cat] = {}

    fast_tails_diff = 452.900
    fast_knuckles_diff = 100.120

    scaled_times = dict.fromkeys(small_stories, [])
    colors = ["#db8720", "#d32c3f", "#dd7de0", "#592c93", "#c46d7a", "#d8d465"]
    cat_colors = dict(zip(small_stories, colors))


    for cat, board in categories.items():
        times = []
        print(board)
        for run in board.runs:
            time = run["run"].times["ingame_t"]

            if time:
                # 2 laps of Super Sonic
                if cat == "Super Sonic's Story":
                    time *= 2
                # Times with fast SADX
                if cat == "Tails' Story":
                    time -= fast_tails_diff
                if cat == "Knuckles' Story":
                    time -= fast_knuckles_diff

                times.append(time)

        category_stats[cat]["count"] = len(times)
        category_stats[cat]["stdev"] = stats.stdev(times)
        category_stats[cat]["wr_t"] = times[0]
        category_stats[cat]["wr"] = str(dt.timedelta(seconds=times[0]))
        category_stats[cat]["median_t"] = stats.median(times)
        category_stats[cat]["median"] = str(dt.timedelta(seconds=stats.median(times)))
        category_stats[cat]["mean_t"] = stats.mean(times)
        category_stats[cat]["mean"] = str(dt.timedelta(seconds=stats.mean(times)))

        scaled_times_l = []
        for time in times:
            scaled_time = (time / times[0]) - 1
            scaled_times_l.append(scaled_time)

        scaled_times[cat] = scaled_times_l

    # pprint(category_stats)

    cat_means = {}
    cat_means_t = {}

    for cat, stat in category_stats.items():
        cat_means[cat] = stat["mean"]
        cat_means_t[cat] = stat["mean_t"]

    pprint(cat_means)
    print()

    combinations = itertools.combinations(cat_means_t.items(), 3)
    combination_durations = [
        [combo, sum(time for _, time in combo)] for combo in combinations
    ]
    shortest_combo = min(combination_durations, key=lambda x: x[1])
    longest_combo = max(combination_durations, key=lambda x: x[1])
    total_duration = sum(duration for _, duration in combination_durations)

    average_duration = str(dt.timedelta(seconds=(total_duration / len(combination_durations))))
    shortest_duration = str(dt.timedelta(seconds=shortest_combo[1]))
    longest_duration = str(dt.timedelta(seconds=longest_combo[1]))

    print("Shortest combination:")
    pprint(shortest_combo)
    print("Longest combination:")
    pprint(longest_combo)
    print()

    print("Shortest duration:", shortest_duration)
    print("Longest duration:", longest_duration)
    print("Average duration:", average_duration)
    print()

    # Calculate seeding weight for each category

    for cat, stat in category_stats.items():
        # Calculate the difference between WR and average
        diff = stat["median_t"] - stat["wr_t"]
        category_stats[cat]["deviation_t"] = diff
        # category_stats[cat]["deviation"] = str(dt.timedelta(seconds=diff))

    pprint(category_stats)

    plot_stats(scaled_times, cat_colors)


def plot_stats(category_stats, cat_colors):
    plt.figure(figsize=(10, 6))

    for category, times in category_stats.items():
        if not times:
            continue  # Skip empty lists
        scaled_times = np.array(times)

        x_normalized = np.linspace(0, 1, len(scaled_times))

        plt.plot(x_normalized, scaled_times, label=category, color=cat_colors.get(category, '#000000'))

    plt.xlabel('Normalized Run Index')
    plt.ylabel('Scaled Time (Relative to WR)')
    plt.title('Speedrun Performance Scaled to World Record')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
