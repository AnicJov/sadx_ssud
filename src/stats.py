import srcomapi, srcomapi.datatypes as srcdt
from pprint import pprint
import statistics as stats
import datetime as dt
import itertools


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
        sadx_runs[category.name] = srcdt.Leaderboard(srcapi, data=srcapi.get("leaderboards/{}/category/{}?embed=variables".format(game.id, category.id)))

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

    for cat, board in categories.items():
        times = []
        for run in board.runs:
            time = run["run"].times["ingame_t"]
            if time:
                times.append(time)
        category_stats[cat]["median_t"] = stats.median(times)
        category_stats[cat]["median"] = str(dt.timedelta(seconds=stats.median(times)))
        category_stats[cat]["mean_t"] = stats.mean(times)
        category_stats[cat]["mean"] = str(dt.timedelta(seconds=stats.mean(times)))

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

    print("Shortest combination:", shortest_combo)
    print("Longest combination:", longest_combo, "\n")

    print("Shortest duration:", shortest_duration)
    print("Longest duration:", longest_duration)
    print("Average duration:", average_duration)


if __name__ == "__main__":
    main()
