# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommendation systems often combine collaborative filtering, which finds patterns in what similar users listen to or enjoy together, with content-based filtering, which matches a user's preferences to song attributes. They can learn from explicit signals such as likes and saves, and implicit signals such as plays, skips, replays, and playlist additions, alongside audio or catalog features. This simulation will focus on content-based recommendations: it compares each song's genre, mood, and audio characteristics with a user's stated taste profile, rather than learning behavior patterns across many users.

- **`Song` fields** (from `data/songs.csv`): `id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`. The first three identify a song; the remaining fields describe its musical style and vibe.
- **Example `UserProfile`** (planned preferences): `{"favorite_genre": "rock", "favorite_mood": "intense", "target_energy": 0.90, "target_tempo_bpm": 150, "target_valence": 0.48, "target_danceability": 0.66, "target_acousticness": 0.10}`. The current dataclass has fewer fields; it will need to be aligned with these targets when the scoring implementation is added.
- **Algorithm Recipe (100 points per song)**:
  - Genre match: **30 points**; mood match: **25 points**. An exact match earns full points; otherwise it earns zero.
  - Numerical proximity: energy **15**, tempo **10**, valence **8**, danceability **7**, and acousticness **5** points maximum per feature.
  - For each numerical feature `f`, calculate `P_f = max(0, 1 - abs(song_f - target_f) / (max_f - min_f))`, where `min_f` and `max_f` are that feature's catalog bounds. Add `weight_f * P_f` points. This rewards closeness to the target, not simply higher or lower values.
- **Ranking Rule**: calculate each song's score, sort scores from highest to lowest, and return the top `k` songs.

```mermaid
flowchart LR
    A["Input: User Profile + songs.csv"] --> B["Process: Score each song"]
    B --> C["Output: Sort and return Top K recommendations"]
```

**Potential biases:** The 30-point genre weight may over-prioritize genre and narrow discovery into a filter bubble. The catalog is small and curated, so its selection may skew which genres and moods can be recommended. Exact genre and mood matching can also miss appealing cross-genre songs.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

```text
Loaded 18 songs.

Top recommendations:

1. Sunrise City - Neon Echo
   Score: 69.59
   Reasons: genre match (+30.0); mood match (+25.0); energy proximity (+14.59)

2. Gym Hero - Max Pulse
   Score: 42.36
   Reasons: genre match (+30.0); energy proximity (+12.36)

3. Rooftop Lights - Indigo Parade
   Score: 39.19
   Reasons: mood match (+25.0); energy proximity (+14.19)

4. Night Drive Loop - Neon Echo
   Score: 13.99
   Reasons: energy proximity (+13.99)

5. Neon Pulse - Vector Bloom
   Score: 13.58
   Reasons: energy proximity (+13.58)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



