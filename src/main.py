"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import argparse
from typing import List, Sequence

try:
    from .recommender import SCORING_STRATEGIES, load_songs, recommend_songs
except ImportError:
    from recommender import SCORING_STRATEGIES, load_songs, recommend_songs


def format_ascii_table(headers: Sequence[str], rows: Sequence[Sequence[str]]) -> str:
    """Render rows as a bordered, column-aligned ASCII table."""
    widths = [len(header) for header in headers]
    for row in rows:
        if len(row) != len(headers):
            raise ValueError("Each table row must have the same number of cells as headers")
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(str(cell)))

    border = "+" + "+".join("-" * (width + 2) for width in widths) + "+"

    def format_row(cells: Sequence[str]) -> str:
        return "| " + " | ".join(
            str(cell).ljust(width) for cell, width in zip(cells, widths)
        ) + " |"

    lines = [border, format_row(headers), border]
    lines.extend(format_row(row) for row in rows)
    lines.append(border)
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare music recommendations across scoring modes.")
    parser.add_argument(
        "--mode",
        action="append",
        choices=SCORING_STRATEGIES,
        help="Scoring mode to run (repeat to compare modes; defaults to balanced, genre_first, and energy_focused).",
    )
    args = parser.parse_args()

    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs.")

    user_prefs = {
        "genre": "metal",
        "mood": "happy",
        "energy": 0.85,
        "popularity": 80,
        "release_decade": 2020,
        "detailed_mood_tags": ["happy", "uplifting", "energetic"],
    }
    modes = args.mode or ["balanced", "genre_first", "energy_focused"]
    print("\nProfile: Metal preference, happy mood, high energy")

    for mode in modes:
        recommendations = recommend_songs(user_prefs, songs, k=8, mode=mode)
        rows: List[List[str]] = [
            [
                str(rank),
                song["title"],
                song.get("artist", ""),
                f"{score:.2f}",
                "; ".join(reasons) if reasons else "No strong preference matches",
            ]
            for rank, (song, score, reasons) in enumerate(recommendations, start=1)
        ]
        print(f"\n{mode.replace('_', ' ').title()} - Top recommendations:")
        print(format_ascii_table(["Rank", "Title", "Artist", "Score", "Reasons"], rows))


if __name__ == "__main__":
    main()
