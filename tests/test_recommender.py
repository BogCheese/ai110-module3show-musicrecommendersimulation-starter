from src.main import print_summary, recommendations_table
from src.recommender import Song, UserProfile, Recommender, recommend_songs

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


# --- Table output (functional path uses plain dicts, as loaded from the CSV) ---

SAMPLE_SONGS = [
    {
        "id": 1, "title": "Test Pop Track", "artist": "Test Artist",
        "genre": "pop", "mood": "happy", "energy": 0.8, "tempo_bpm": 120.0,
        "valence": 0.9, "danceability": 0.8, "acousticness": 0.2,
    },
    {
        "id": 2, "title": "Chill Lofi Loop", "artist": "Test Artist",
        "genre": "lofi", "mood": "chill", "energy": 0.4, "tempo_bpm": 80.0,
        "valence": 0.6, "danceability": 0.5, "acousticness": 0.9,
    },
]
FULL_PREFS = {
    "genre": "pop", "mood": "happy",
    "energy": 0.8, "valence": 0.9, "acousticness": 0.2,
}


def test_table_includes_every_song_score_and_reason():
    results = recommend_songs(FULL_PREFS, SAMPLE_SONGS, k=2)
    table = recommendations_table(FULL_PREFS, results)

    for song, score, explanation in results:
        assert song["title"] in table
        assert f"{score:.2f}" in table
        for reason in explanation.split("; "):
            assert reason in table


def test_table_shows_the_most_this_profile_can_score():
    no_labels = {"energy": 0.8, "valence": 0.9, "acousticness": 0.2}  # no mood or genre
    results = recommend_songs(no_labels, SAMPLE_SONGS, k=2)

    assert "/ 5.0" in recommendations_table(no_labels, results)
    assert "/ 9.0" in recommendations_table(FULL_PREFS, recommend_songs(FULL_PREFS, SAMPLE_SONGS, k=2))


def test_summary_lists_every_profile_and_handles_a_single_result(capsys):
    two = recommend_songs(FULL_PREFS, SAMPLE_SONGS, k=2)
    one = recommend_songs(FULL_PREFS, SAMPLE_SONGS, k=1)
    print_summary([("Profile One", FULL_PREFS, two), ("Profile Two", FULL_PREFS, one)])

    output = capsys.readouterr().out
    assert "Profile One" in output
    assert "Profile Two" in output
    assert "Test Pop Track" in output
