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
- **`UserProfile` preferences**: `favorite_genre` (matched to `genre`), `favorite_mood` (matched to `mood`), and target values for `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`.
- **Scoring Rule**: score one song on a 0–1 scale using weighted feature matches: genre 30%, mood 25%, energy 15%, tempo 10%, valence 8%, danceability 7%, and acousticness 5%. Genre and mood receive full credit for a match; numerical features earn more credit as they get closer to the user's target, using normalized distance rather than rewarding simply higher or lower values.
- **Ranking Rule**: score every eligible song, sort by score from highest to lowest, and return the top `k` songs as recommendations.

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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
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



