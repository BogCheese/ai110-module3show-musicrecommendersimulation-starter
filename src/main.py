"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


MAX_SCORE = 9.0  # mood 3 + valence 2 + energy 2 + acousticness 1 + genre 1
WIDTH = 64


def print_recommendations(user_prefs: dict, recommendations: list) -> None:
    """Print ranked recommendations with the score and one reason per line."""
    profile = ", ".join(f"{key} {value}" for key, value in user_prefs.items())

    print()
    print("=" * WIDTH)
    print(f" TOP {len(recommendations)} RECOMMENDATIONS")
    print(f" Profile: {profile}")
    print("=" * WIDTH)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print()
        print(f"#{rank}  {song['title']} - {song['artist']}")
        print(f"    {song['genre']} | {song['mood']}")
        print(f"    Score: {score:.2f} / {MAX_SCORE:.1f}")
        print("    Why:")
        for reason in explanation.split("; "):
            print(f"      - {reason}")
        print("-" * WIDTH)


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # "Rainy Day" taste profile: calm, sad, acoustic
    user_prefs = {
        "genre": "folk",
        "mood": "sad",
        "energy": 0.30,
        "valence": 0.25,
        "acousticness": 0.85,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_recommendations(user_prefs, recommendations)


if __name__ == "__main__":
    main()
