from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

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
        """Return the top k songs ranked for a user's profile."""
        catalog = [
            {
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "tempo_bpm": song.tempo_bpm,
                "valence": song.valence,
                "danceability": song.danceability,
                "acousticness": song.acousticness,
            }
            for song in self.songs
        ]
        prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        if user.likes_acoustic:
            prefs["acousticness"] = 1.0

        ranked = []
        for song, song_data in zip(self.songs, catalog):
            score, _ = score_song(prefs, song_data)
            ranked.append((score, song))
        ranked.sort(key=lambda item: item[0], reverse=True)
        return [song for _, song in ranked[:max(k, 0)]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a readable explanation of a song's score."""
        prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        if user.likes_acoustic:
            prefs["acousticness"] = 1.0
        song_data = {
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "tempo_bpm": song.tempo_bpm,
            "valence": song.valence,
            "danceability": song.danceability,
            "acousticness": song.acousticness,
        }
        _, reasons = score_song(prefs, song_data)
        return "; ".join(reasons) if reasons else "No strong preference matches"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and convert numeric features to numbers."""
    numeric_columns = {
        "id": int,
        "energy": float,
        "tempo_bpm": float,
        "valence": float,
        "danceability": float,
        "acousticness": float,
    }
    songs = []
    with open(csv_path, "r", encoding="utf-8", newline="") as csv_file:
        for row in csv.DictReader(csv_file):
            song = {}
            for column, value in row.items():
                if column in numeric_columns:
                    song[column] = numeric_columns[column](value)
                else:
                    song[column] = value
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against a user profile and return its points and reasons."""
    score = 0.0
    reasons = []

    favorite_genre = user_prefs.get("genre", user_prefs.get("favorite_genre"))
    if favorite_genre and str(song.get("genre", "")).lower() == str(favorite_genre).lower():
        score += 30.0
        reasons.append("genre match (+30.0)")

    favorite_mood = user_prefs.get("mood", user_prefs.get("favorite_mood"))
    if favorite_mood and str(song.get("mood", "")).lower() == str(favorite_mood).lower():
        score += 25.0
        reasons.append("mood match (+25.0)")

    feature_weights = {
        "energy": 15.0,
        "tempo_bpm": 10.0,
        "valence": 8.0,
        "danceability": 7.0,
        "acousticness": 5.0,
    }
    catalog_bounds = {
        "energy": (0.22, 0.96),
        "tempo_bpm": (60.0, 168.0),
        "valence": (0.31, 0.90),
        "danceability": (0.25, 0.91),
        "acousticness": (0.04, 0.95),
    }
    for feature, weight in feature_weights.items():
        target = user_prefs.get(feature, user_prefs.get(f"target_{feature}"))
        if target is None:
            continue
        minimum, maximum = catalog_bounds[feature]
        span = maximum - minimum
        proximity = max(0.0, 1.0 - abs(float(song[feature]) - float(target)) / span) if span else 0.0
        points = weight * proximity
        score += points
        if points > 0:
            reasons.append(f"{feature.replace('_bpm', '')} proximity (+{points:.2f})")

    return round(score, 10), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Rank songs for a user profile and return the highest-scoring k results."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, reasons))
    scored.sort(key=lambda result: result[1], reverse=True)
    limit = max(k, 0)
    return [(song, score, reasons) for song, score, reasons in scored[:limit]]
