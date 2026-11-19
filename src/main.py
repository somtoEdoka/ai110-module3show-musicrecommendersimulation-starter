"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from .recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs.")

    profiles = [
        ("High-Energy Pop", {"genre": "pop", "mood": "happy", "energy": 0.85}),
        ("Chill Lofi", {"genre": "lofi", "mood": "chill", "energy": 0.40}),
        ("Deep Intense Rock", {"genre": "rock", "mood": "intense", "energy": 0.90}),
        (
            "Conflicting: Unseen Genre, Sad Mood, High Energy",
            {"genre": "shoegaze", "mood": "sad", "energy": 0.90},
        ),
    ]

    for profile_name, user_prefs in profiles:
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\n{profile_name} — Top recommendations:\n")
        for rank, (song, score, reasons) in enumerate(recommendations, start=1):
            artist = f" - {song['artist']}" if song.get("artist") else ""
            print(f"{rank}. {song['title']}{artist}")
            print(f"   Score: {score:.2f}")
            print(f"   Reasons: {'; '.join(reasons) if reasons else 'No strong preference matches'}")
            print()


if __name__ == "__main__":
    main()
