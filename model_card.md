# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

The catalog contains only 18 hand-curated songs, with many genres and moods represented by just one song, so recommendations reflect the catalog's gaps rather than the full range of music. An exact genre match is worth 30 points and an exact mood match is worth 25, which can outweigh close audio-feature matches and may keep users in a narrow genre or mood. When a profile asks for an unseen genre and mood, as in our adversarial test, neither preference can match; the results are then driven by the one available numeric preference, energy. The top-five list has no artist or style diversity rule, so similar songs can crowd out less obvious discoveries.

---

## 7. Evaluation  

We ran `python -m src.main` for four profiles: **High-Energy Pop**, **Chill Lofi**, **Deep Intense Rock**, and the adversarial **Conflicting: Unseen Genre, Sad Mood, High Energy** profile. We checked whether songs with matching genre and mood appeared near the top, whether high-energy profiles received energetic songs, and how the conflicting profile behaved when its requested labels were absent from the catalog.

### Baseline terminal output

```text
Loaded 18 songs.

High-Energy Pop — Top recommendations:

1. Sunrise City - Neon Echo
   Score: 69.39
   Reasons: genre match (+30.0); mood match (+25.0); energy proximity (+14.39)

2. Gym Hero - Max Pulse
   Score: 43.38
   Reasons: genre match (+30.0); energy proximity (+13.38)

3. Rooftop Lights - Indigo Parade
   Score: 38.18
   Reasons: mood match (+25.0); energy proximity (+13.18)

4. Neon Pulse - Vector Bloom
   Score: 14.59
   Reasons: energy proximity (+14.59)

5. Paper Crown - Static Youth
   Score: 14.19
   Reasons: energy proximity (+14.19)


Chill Lofi — Top recommendations:

1. Midnight Coding - LoRoom
   Score: 69.59
   Reasons: genre match (+30.0); mood match (+25.0); energy proximity (+14.59)

2. Library Rain - Paper Lanterns
   Score: 68.99
   Reasons: genre match (+30.0); mood match (+25.0); energy proximity (+13.99)

3. Focus Flow - LoRoom
   Score: 45.00
   Reasons: genre match (+30.0); energy proximity (+15.00)

4. Spacewalk Thoughts - Orbit Bloom
   Score: 37.57
   Reasons: mood match (+25.0); energy proximity (+12.57)

5. Coffee Shop Stories - Slow Stereo
   Score: 14.39
   Reasons: energy proximity (+14.39)


Deep Intense Rock — Top recommendations:

1. Storm Runner - Voltline
   Score: 69.80
   Reasons: genre match (+30.0); mood match (+25.0); energy proximity (+14.80)

2. Gym Hero - Max Pulse
   Score: 39.39
   Reasons: mood match (+25.0); energy proximity (+14.39)

3. Paper Crown - Static Youth
   Score: 14.80
   Reasons: energy proximity (+14.80)

4. Neon Pulse - Vector Bloom
   Score: 14.39
   Reasons: energy proximity (+14.39)

5. Iron Horizon - Black Meridian
   Score: 13.78
   Reasons: energy proximity (+13.78)


Conflicting: Unseen Genre, Sad Mood, High Energy — Top recommendations:

1. Storm Runner - Voltline
   Score: 14.80
   Reasons: energy proximity (+14.80)

2. Paper Crown - Static Youth
   Score: 14.80
   Reasons: energy proximity (+14.80)

3. Gym Hero - Max Pulse
   Score: 14.39
   Reasons: energy proximity (+14.39)

4. Neon Pulse - Vector Bloom
   Score: 14.39
   Reasons: energy proximity (+14.39)

5. Iron Horizon - Black Meridian
   Score: 13.78
   Reasons: energy proximity (+13.78)
```

### What we observed

The recommendations felt sensible when a profile's genre and mood both exist in the catalog: for example, the Chill Lofi list begins with two songs matching both labels, and the Deep Intense Rock list begins with a song matching both rock and intense. The High-Energy Pop result also fit its preferences. Storm Runner ranked first for Deep Intense Rock because it received the full 30 genre points and 25 mood points, with an additional 14.80 points for being near the energy target. It was notable that the conflicting profile still produced a confident-looking ranked list even though none of its requested genre or mood labels matched; every reason shown was energy proximity.

### Pairwise profile comparisons

- **High-Energy Pop vs. Chill Lofi:** The pop profile favors Sunrise City and Gym Hero, while the lofi profile favors Midnight Coding, Library Rain, and Focus Flow. This makes sense because each profile's exact genre and mood matches earn large bonuses; the lower target energy also helps the calmer lofi songs.
- **High-Energy Pop vs. Deep Intense Rock:** Sunrise City wins for pop/happy, whereas Storm Runner wins for rock/intense. Gym Hero appears in both lists because it is pop and energetic, and it also matches the intense mood even though its genre is not rock.
- **High-Energy Pop vs. the conflicting profile:** The pop profile has exact genre and mood matches, which place Sunrise City first. The conflicting profile has no matching labels, so its recommendations are determined only by closeness to high energy, with Storm Runner and Paper Crown tied at the top.
- **Chill Lofi vs. Deep Intense Rock:** The chill profile favors lofi/chill songs around energy 0.40, while the rock profile favors Storm Runner, which matches rock/intense and has high energy. Their shared high-scoring rule is the exact-match bonus, applied to different labels.
- **Chill Lofi vs. the conflicting profile:** Lofi/chill receives two exact-match bonuses, giving Midnight Coding and Library Rain large leads. The conflicting profile receives neither bonus, so higher-energy songs rise based on energy closeness.
- **Deep Intense Rock vs. the conflicting profile:** Both ask for high energy, so their lists overlap on Storm Runner, Paper Crown, Gym Hero, Neon Pulse, and Iron Horizon. Storm Runner receives both exact-match bonuses only for the rock profile; in the conflicting list it earns energy points alone.

### Weight Shift sensitivity experiment

We temporarily changed genre weight from 30 to 15 points and energy weight from 15 to 30 points, leaving the other scoring rules unchanged. This shifted songs with closer energy to the front when the genre bonus had been deciding close contests. The experiment output was:

```text
Loaded 18 songs.

High-Energy Pop — Top recommendations:

1. Sunrise City - Neon Echo
   Score: 68.78
   Reasons: genre match (+15.0); mood match (+25.0); energy proximity (+28.78)

2. Rooftop Lights - Indigo Parade
   Score: 51.35
   Reasons: mood match (+25.0); energy proximity (+26.35)

3. Gym Hero - Max Pulse
   Score: 41.76
   Reasons: genre match (+15.0); energy proximity (+26.76)

4. Neon Pulse - Vector Bloom
   Score: 29.19
   Reasons: energy proximity (+29.19)

5. Paper Crown - Static Youth
   Score: 28.38
   Reasons: energy proximity (+28.38)


Chill Lofi — Top recommendations:

1. Midnight Coding - LoRoom
   Score: 69.19
   Reasons: genre match (+15.0); mood match (+25.0); energy proximity (+29.19)

2. Library Rain - Paper Lanterns
   Score: 67.97
   Reasons: genre match (+15.0); mood match (+25.0); energy proximity (+27.97)

3. Spacewalk Thoughts - Orbit Bloom
   Score: 50.14
   Reasons: mood match (+25.0); energy proximity (+25.14)

4. Focus Flow - LoRoom
   Score: 45.00
   Reasons: genre match (+15.0); energy proximity (+30.00)

5. Coffee Shop Stories - Slow Stereo
   Score: 28.78
   Reasons: energy proximity (+28.78)


Deep Intense Rock — Top recommendations:

1. Storm Runner - Voltline
   Score: 69.59
   Reasons: genre match (+15.0); mood match (+25.0); energy proximity (+29.59)

2. Gym Hero - Max Pulse
   Score: 53.78
   Reasons: mood match (+25.0); energy proximity (+28.78)

3. Paper Crown - Static Youth
   Score: 29.59
   Reasons: energy proximity (+29.59)

4. Neon Pulse - Vector Bloom
   Score: 28.78
   Reasons: energy proximity (+28.78)

5. Iron Horizon - Black Meridian
   Score: 27.57
   Reasons: energy proximity (+27.57)


Conflicting: Unseen Genre, Sad Mood, High Energy — Top recommendations:

1. Storm Runner - Voltline
   Score: 29.59
   Reasons: energy proximity (+29.59)

2. Paper Crown - Static Youth
   Score: 29.59
   Reasons: energy proximity (+29.59)

3. Gym Hero - Max Pulse
   Score: 28.78
   Reasons: energy proximity (+28.78)

4. Neon Pulse - Vector Bloom
   Score: 28.78
   Reasons: energy proximity (+28.78)

5. Iron Horizon - Black Meridian
   Score: 27.57
   Reasons: energy proximity (+27.57)
```

In the shifted run, Rooftop Lights moved above Gym Hero for High-Energy Pop, and Spacewalk Thoughts moved above Focus Flow for Chill Lofi. The Deep Intense Rock and conflicting profile rankings stayed in the same order, but their scores changed. The baseline weights were restored after the experiment.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
