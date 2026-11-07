import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read a songs CSV into a list of dicts, converting numeric columns to int/float."""
    int_fields = ("id",)
    float_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

# Points available per feature (total 9.0). Mood is weighted above genre
# because mood is how I describe a vibe and genre is sparse in the catalog.
WEIGHTS = {"mood": 3.0, "valence": 2.0, "energy": 2.0, "acousticness": 1.0, "genre": 1.0}

# Moods grouped into families so similar moods earn partial credit
# (for example chill and relaxed). moody and romantic are standalone.
MOOD_FAMILIES = {
    "low": {"sad", "melancholic", "bittersweet"},
    "calm": {"chill", "relaxed", "focused", "nostalgic"},
    "upbeat": {"happy", "uplifting", "festive", "euphoric"},
    "intense": {"intense", "angry", "confident"},
}
# Families that sit next to each other on the calm-to-intense spectrum.
NEIGHBOR_FAMILIES = {
    frozenset({"low", "calm"}),
    frozenset({"calm", "upbeat"}),
    frozenset({"upbeat", "intense"}),
}


def mood_credit(target: str, song_mood: str) -> float:
    """Return mood credit from 0 to 1: exact 1.0, same family 0.8, neighbor family 0.3."""
    if target == song_mood:
        return 1.0
    fam_target = next((f for f, moods in MOOD_FAMILIES.items() if target in moods), None)
    fam_song = next((f for f, moods in MOOD_FAMILIES.items() if song_mood in moods), None)
    if fam_target is None or fam_song is None:
        return 0.0
    if fam_target == fam_song:
        return 0.8
    if frozenset({fam_target, fam_song}) in NEIGHBOR_FAMILIES:
        return 0.3
    return 0.0


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song (max 9.0) by closeness to the user's prefs; return (score, reasons)."""
    reasons: List[str] = []
    total = 0.0

    # Mood: exact match, same family, or neighboring family.
    if "mood" in user_prefs:
        credit = mood_credit(user_prefs["mood"], song["mood"])
        points = WEIGHTS["mood"] * credit
        total += points
        if credit == 1.0:
            reasons.append(f"mood match: {song['mood']} (+{points:.1f})")
        elif credit > 0:
            reasons.append(
                f"similar mood: {song['mood']} ~ {user_prefs['mood']} (+{points:.1f})"
            )

    # Numeric features: reward closeness to the user's target.
    for key in ("valence", "energy", "acousticness"):
        if key in user_prefs:
            closeness = max(0.0, 1.0 - abs(song[key] - user_prefs[key]))
            points = WEIGHTS[key] * closeness
            total += points
            reasons.append(
                f"{key} close: {song[key]:.2f} vs target {user_prefs[key]:.2f} "
                f"(+{points:.1f})"
            )

    # Genre: exact match only, smallest weight.
    if "genre" in user_prefs and song["genre"] == user_prefs["genre"]:
        total += WEIGHTS["genre"]
        reasons.append(f"genre match: {song['genre']} (+{WEIGHTS['genre']:.1f})")

    return round(total, 2), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top k as (song, score, explanation), best first."""
    # Judge every song with score_song, keeping (song, score, reasons).
    scored = [(song, *score_song(user_prefs, song)) for song in songs]

    # sorted() returns a new list and leaves `scored` untouched. Ties are
    # broken by mood credit (higher first), then by title (A to Z).
    ranked = sorted(
        scored,
        key=lambda item: (
            -item[1],
            -mood_credit(user_prefs.get("mood"), item[0]["mood"]),
            item[0]["title"],
        ),
    )

    return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked[:k]]
