"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, max_score, recommend_songs


WIDTH = 64


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


def print_recommendations(name: str, user_prefs: dict, recommendations: list) -> None:
    """Print ranked recommendations with the score and one reason per line."""
    profile = ", ".join(f"{key} {value}" for key, value in user_prefs.items())

    print()
    print("=" * WIDTH)
    print(f" {name.upper()}: TOP {len(recommendations)} RECOMMENDATIONS")
    print(f" Profile: {profile}")
    print("=" * WIDTH)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print()
        print(f"#{rank}  {song['title']} - {song['artist']}")
        print(f"    {song['genre']} | {song['mood']}")
        print(f"    Score: {score:.2f} / {max_score(user_prefs):.1f}")
        print("    Why:")
        for reason in explanation.split("; "):
            print(f"      - {reason}")
        print("-" * WIDTH)


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(name, user_prefs, recommendations)


if __name__ == "__main__":
    main()
