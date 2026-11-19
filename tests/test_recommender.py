from pathlib import Path

from src.main import format_ascii_table
from src.recommender import Song, UserProfile, Recommender, load_songs, recommend_songs, score_song

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


def test_load_songs_parses_advanced_fields():
    catalog_path = Path(__file__).parent.parent / "data" / "songs.csv"
    songs = load_songs(str(catalog_path))

    assert len(songs) == 18
    assert isinstance(songs[0]["popularity"], int)
    assert isinstance(songs[0]["release_decade"], int)
    assert isinstance(songs[0]["time_signature"], int)
    assert isinstance(songs[0]["detailed_mood_tags"], list)
    assert songs[0]["detailed_mood_tags"] == ["happy", "uplifting", "energetic"]


def test_scoring_modes_can_change_rankings_for_the_same_profile():
    songs = [
        {"title": "Genre match", "genre": "pop", "mood": "calm"},
        {"title": "Mood match", "genre": "rock", "mood": "happy"},
    ]
    profile = {"genre": "pop", "mood": "happy"}

    balanced = recommend_songs(profile, songs, k=2, mode="balanced")
    mood_first = recommend_songs(profile, songs, k=2, mode="mood_first")

    assert balanced[0][0]["title"] == "Genre match"
    assert mood_first[0][0]["title"] == "Mood match"


def test_advanced_preferences_add_scores_and_explanations():
    song = {
        "popularity": 80,
        "release_decade": 2020,
        "detailed_mood_tags": ["happy", "uplifting"],
        "key": "C",
        "time_signature": 4,
    }
    profile = {
        "popularity": 80,
        "release_decade": 2020,
        "detailed_mood_tags": ["happy", "energetic"],
        "key": "c",
        "time_signature": 4,
    }

    score, reasons = score_song(profile, song)

    assert score == 21.0
    assert len(reasons) == 5
    assert any("detailed mood tags match" in reason for reason in reasons)


def test_recommend_songs_greedily_penalizes_repeat_artists():
    songs = [
        {"title": "First Echo song", "artist": "Echo", "genre": "pop"},
        {"title": "Second Echo song", "artist": "Echo", "genre": "pop"},
        {"title": "Solo song", "artist": "Solo", "genre": "pop"},
    ]

    recommendations = recommend_songs({"genre": "pop"}, songs, k=3)

    assert [song["title"] for song, _, _ in recommendations] == [
        "First Echo song",
        "Solo song",
        "Second Echo song",
    ]
    assert recommendations[2][1] == 29.5
    assert "diversity penalty (-0.50: repeat artist)" in recommendations[2][2]


def test_ascii_table_is_bordered_and_aligned():
    table = format_ascii_table(
        ["Rank", "Title", "Artist", "Score", "Reasons"],
        [["1", "Song", "Artist", "3.00", "example reason"]],
    )
    lines = table.splitlines()

    assert lines[0].startswith("+") and lines[0].endswith("+")
    assert "| Rank" in lines[1] and "Reasons" in lines[1]
    assert len({len(line) for line in lines}) == 1
