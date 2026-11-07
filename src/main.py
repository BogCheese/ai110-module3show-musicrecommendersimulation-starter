"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from tabulate import tabulate

from src.recommender import load_songs, max_score, recommend_songs


# Taste profiles. Each is a dict of target values (see score_song for the keys).
PROFILES = {
    # --- Distinct, realistic tastes ---
    "High-Energy Pop": {
        "genre": "pop", "mood": "happy",
        "energy": 0.85, "valence": 0.80, "acousticness": 0.15,
    },
    "Chill Lofi": {
        "genre": "lofi", "mood": "chill",
        "energy": 0.38, "valence": 0.58, "acousticness": 0.80,
    },
    "Deep Intense Rock": {
        "genre": "rock", "mood": "intense",
        "energy": 0.92, "valence": 0.45, "acousticness": 0.08,
    },
    "Rainy Day": {
        "genre": "folk", "mood": "sad",
        "energy": 0.30, "valence": 0.25, "acousticness": 0.85,
    },
    # --- Adversarial / edge cases: can the scoring be tricked? ---
    "Sad Banger (conflicting)": {  # sad mood but very high energy
        "genre": "pop", "mood": "sad",
        "energy": 0.90, "valence": 0.20, "acousticness": 0.10,
    },
    "Genre Trap (lofi but intense)": {  # genre says calm, everything else says loud
        "genre": "lofi", "mood": "intense",
        "energy": 0.95, "valence": 0.50, "acousticness": 0.05,
    },
    "Unknown Mood and Genre": {  # values that exist nowhere in the catalog
        "genre": "k-pop", "mood": "mysterious",
        "energy": 0.60, "valence": 0.60, "acousticness": 0.50,
    },
    "Dead Center (no mood/genre)": {  # every target in the middle, no labels
        "energy": 0.50, "valence": 0.50, "acousticness": 0.50,
    },
}


def make_table(rows: list, headers: list, colalign: tuple) -> str:
    """Build an ASCII grid table. disable_numparse keeps scores like '8.86 / 9.0' as typed."""
    return tabulate(
        rows,
        headers=headers,
        tablefmt="grid",
        colalign=colalign,
        disable_numparse=True,
    )


def print_banner(title_lines: list, width: int) -> None:
    """Print title lines between two '=' rules of the given width."""
    print()
    print("=" * width)
    for line in title_lines:
        print(f" {line}")
    print("=" * width)


def recommendations_table(user_prefs: dict, recommendations: list) -> str:
    """Table of rank, song, score, and every reason (one per line) for each recommendation."""
    ceiling = max_score(user_prefs)
    rows = []
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        rows.append([
            rank,
            f"{song['title']}\n{song['artist']}\n{song['genre']} | {song['mood']}",
            f"{score:.2f} / {ceiling:.1f}",
            "\n".join(f"- {reason}" for reason in explanation.split("; ")),
        ])
    return make_table(
        rows,
        headers=["#", "Song", "Score", "Reasons"],
        colalign=("center", "left", "center", "left"),
    )


def print_recommendations(name: str, user_prefs: dict, recommendations: list) -> None:
    """Print one profile's top picks as a table, including the reasons for each score."""
    profile = ", ".join(f"{key} {value}" for key, value in user_prefs.items())
    table = recommendations_table(user_prefs, recommendations)
    width = max(len(line) for line in table.splitlines())

    print_banner(
        [f"{name.upper()}: TOP {len(recommendations)} RECOMMENDATIONS", f"Profile: {profile}"],
        width,
    )
    print(table)


def print_summary(results: list) -> None:
    """Print one row per profile with its top pick and runner-up, to compare profiles at a glance."""
    rows = []
    for name, user_prefs, recommendations in results:
        ceiling = max_score(user_prefs)
        row = [name]
        for index in (0, 1):
            if index < len(recommendations):
                song, score, _ = recommendations[index]
                row += [song["title"], f"{score:.2f} / {ceiling:.1f}"]
            else:
                row += ["-", "-"]
        rows.append(row)

    table = make_table(
        rows,
        headers=["Profile", "Top pick", "Score", "Runner-up", "Score"],
        colalign=("left", "left", "center", "left", "center"),
    )
    print_banner(["SUMMARY OF ALL PROFILES"], max(len(line) for line in table.splitlines()))
    print(table)


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    results = []
    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(name, user_prefs, recommendations)
        results.append((name, user_prefs, recommendations))

    print_summary(results)


if __name__ == "__main__":
    main()
