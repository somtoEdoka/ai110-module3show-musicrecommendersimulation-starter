from typing import List, Dict, Tuple
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
        "popularity": int,
        "release_decade": int,
        "time_signature": int,
    }
    songs = []
    with open(csv_path, "r", encoding="utf-8", newline="") as csv_file:
        for row in csv.DictReader(csv_file):
            song = {}
            for column, value in row.items():
                if column in numeric_columns:
                    song[column] = numeric_columns[column](value)
                elif column == "detailed_mood_tags":
                    song[column] = [tag.strip() for tag in value.split("|") if tag.strip()]
                else:
                    song[column] = value
            songs.append(song)
    return songs

SCORING_STRATEGIES = {
    "balanced": {
        "genre": 30.0, "mood": 25.0, "energy": 15.0, "tempo_bpm": 10.0,
        "valence": 8.0, "danceability": 7.0, "acousticness": 5.0,
        "popularity": 5.0, "release_decade": 5.0,
        "detailed_mood_tags": 10.0, "key": 3.0, "time_signature": 3.0,
    },
    "genre_first": {
        "genre": 50.0, "mood": 15.0, "energy": 10.0, "tempo_bpm": 7.0,
        "valence": 5.0, "danceability": 5.0, "acousticness": 3.0,
        "popularity": 4.0, "release_decade": 3.0,
        "detailed_mood_tags": 6.0, "key": 1.0, "time_signature": 1.0,
    },
    "mood_first": {
        "genre": 15.0, "mood": 50.0, "energy": 10.0, "tempo_bpm": 7.0,
        "valence": 5.0, "danceability": 5.0, "acousticness": 3.0,
        "popularity": 4.0, "release_decade": 3.0,
        "detailed_mood_tags": 8.0, "key": 1.0, "time_signature": 1.0,
    },
    "energy_focused": {
        "genre": 15.0, "mood": 10.0, "energy": 45.0, "tempo_bpm": 15.0,
        "valence": 5.0, "danceability": 5.0, "acousticness": 2.0,
        "popularity": 2.0, "release_decade": 2.0,
        "detailed_mood_tags": 2.0, "key": 1.0, "time_signature": 1.0,
    },
}

NUMERICAL_BOUNDS = {
    "energy": (0.22, 0.96),
    "tempo_bpm": (60.0, 168.0),
    "valence": (0.31, 0.90),
    "danceability": (0.25, 0.91),
    "acousticness": (0.04, 0.95),
    "popularity": (0.0, 100.0),
    "release_decade": (2000.0, 2020.0),
}


def score_song(
    user_prefs: Dict, song: Dict, mode: str = "balanced"
) -> Tuple[float, List[str]]:
    """Score one song using the selected strategy and explain its points."""
    if mode not in SCORING_STRATEGIES:
        raise ValueError(f"Unknown scoring mode {mode!r}; choose from {', '.join(SCORING_STRATEGIES)}")

    weights = SCORING_STRATEGIES[mode]
    score = 0.0
    reasons = []

    favorite_genre = user_prefs.get("genre", user_prefs.get("favorite_genre"))
    if favorite_genre and str(song.get("genre", "")).lower() == str(favorite_genre).lower():
        score += weights["genre"]
        reasons.append(f"genre match (+{weights['genre']:.1f})")

    favorite_mood = user_prefs.get("mood", user_prefs.get("favorite_mood"))
    if favorite_mood and str(song.get("mood", "")).lower() == str(favorite_mood).lower():
        score += weights["mood"]
        reasons.append(f"mood match (+{weights['mood']:.1f})")

    for feature, (minimum, maximum) in NUMERICAL_BOUNDS.items():
        target = user_prefs.get(feature, user_prefs.get(f"target_{feature}"))
        if target is None or feature not in song:
            continue
        span = maximum - minimum
        proximity = max(0.0, 1.0 - abs(float(song[feature]) - float(target)) / span)
        points = weights[feature] * proximity
        score += points
        if points > 0:
            label = feature.replace("_bpm", "")
            reasons.append(f"{label} proximity (+{points:.2f})")

    target_tags = user_prefs.get("detailed_mood_tags", user_prefs.get("mood_tags"))
    song_tags = song.get("detailed_mood_tags")
    if target_tags and song_tags is not None:
        if isinstance(target_tags, str):
            target_tags = target_tags.split("|")
        requested = {str(tag).strip().lower() for tag in target_tags if str(tag).strip()}
        available = {str(tag).strip().lower() for tag in song_tags if str(tag).strip()}
        if requested:
            tag_match = len(requested & available) / len(requested)
            points = weights["detailed_mood_tags"] * tag_match
            score += points
            if points > 0:
                reasons.append(f"detailed mood tags match (+{points:.2f})")

    for feature in ("key", "time_signature"):
        target = user_prefs.get(feature)
        if target is None or song.get(feature) is None:
            continue
        if str(song[feature]).strip().lower() == str(target).strip().lower():
            points = weights[feature]
            score += points
            reasons.append(f"{feature.replace('_', ' ')} match (+{points:.1f})")

    return round(score, 10), reasons

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = "balanced",
    diversity_penalty: float = 0.5,
) -> List[Tuple[Dict, float, List[str]]]:
    """Greedily rank songs, penalizing artists already selected."""
    if diversity_penalty < 0:
        raise ValueError("diversity_penalty must be non-negative")

    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, mode=mode)
        scored.append((song, score, reasons))

    limit = max(k, 0)
    recommendations = []
    selected_artists = set()
    while scored and len(recommendations) < limit:
        best_index = 0
        best_score = float("-inf")
        best_reasons = []
        for index, (song, base_score, base_reasons) in enumerate(scored):
            effective_score = base_score
            reasons = base_reasons
            artist = str(song.get("artist", "")).strip()
            normalized_artist = artist.casefold()
            if normalized_artist and normalized_artist in selected_artists and diversity_penalty:
                effective_score -= diversity_penalty
                reasons = [
                    *base_reasons,
                    f"diversity penalty (-{diversity_penalty:.2f}: repeat artist)",
                ]
            if effective_score > best_score:
                best_index = index
                best_score = effective_score
                best_reasons = reasons

        song, _, _ = scored.pop(best_index)
        recommendations.append((song, round(best_score, 10), best_reasons))
        artist = str(song.get("artist", "")).strip()
        if artist:
            selected_artists.add(artist.casefold())

    return recommendations
