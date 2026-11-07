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

Real-world recommenders like Spotify and YouTube combine two kinds of signals: what other people with similar behavior enjoyed (collaborative filtering), and what the songs themselves sound like (content-based filtering). They turn those signals into a score for every candidate song, then rank the scores to decide what to show. My version is a simplified, purely content-based recommender: it has no data about other users, so it works only from song attributes and one fixed user taste profile. Each song gets a score from 0 to 1 that rewards *closeness* to the user's preferences instead of simply higher or lower values. I prioritize **mood** most heavily, since that is how I naturally describe a vibe. Next come **valence and energy**, with **acousticness** and **genre** as smaller tie-breakers. Mood uses partial credit so that similar moods such as chill and relaxed still count as a match. Everything is a soft score with no hard filters, so a song that misses on one feature can still rank well overall. After scoring every song, the system sorts by score and returns the top results.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

### Data flow

```
INPUT                    PROCESS (the loop)                       OUTPUT
-----                    ------------------                       ------
User taste profile  -->  for each song in data/songs.csv:    -->  sort by score (high to low)
(one fixed dict)           1. load the row as a Song               break ties: mood score, then title
                           2. score it against the profile         keep the top k (default 5)
                           3. store (song, score, explanation)     show each song with its reasons
```

### Features used

- **`Song`** (from `data/songs.csv`): `mood`, `valence`, `energy`, `acousticness` and `genre` are scored. `id`, `title` and `artist` are for display. `tempo_bpm` and `danceability` are loaded but not scored (redundant with energy, or a weak signal).
- **`UserProfile`**: one fixed taste with `favorite_mood`, `target_valence`, `target_energy`, `target_acousticness` and `favorite_genre`. Example, a "Rainy Day" taste: mood `sad`, valence 0.25, energy 0.30, acousticness 0.85, genre `folk`.

### Algorithm Recipe

**Scoring Rule** (one song vs. the profile, result from 0 to 1):

| Component | Weight | How it is computed |
|---|---|---|
| Mood | 3.0 | Partial credit by mood family: exact match 1.0, close mood about 0.8, loosely related 0.3-0.5, unrelated 0 (so chill and relaxed still match) |
| Valence | 2.0 | `1 - abs(song_valence - target_valence)` |
| Energy | 2.0 | `1 - abs(song_energy - target_energy)` |
| Acousticness | 1.0 | `1 - abs(song_acousticness - target_acousticness)` |
| Genre | 1.0 | 1.0 for an exact match, otherwise 0 |

`score = sum(weight x component) / 9.0`

Numeric features reward *closeness* to the target, not higher or lower values. Everything is a soft score with no hard filters.

**Ranking Rule** (the whole catalog): score every song, sort from highest to lowest, break ties by mood score and then title, and return the top k with a short explanation of what contributed to each score.

**Why mood outweighs genre:** mood is how I naturally describe a vibe, and genre is too sparse in this catalog to carry much weight (most genres appear in only one song).

### Expected biases and limitations

- **Mood dominance:** with the largest weight, a mood match can lift a song whose numbers fit poorly, and a great song with a differently labeled mood gets penalized. Results also depend on my hand-made mood-similarity map.
- **Valence cannot tell sad from angry:** both are low valence, so only energy, acousticness and mood separate them.
- **Acoustic bias:** a high acousticness target penalizes electronic songs, even sad ones.
- **One fixed taste:** the profile cannot say "sad when coding, intense at the gym". Multiple contexts are future work.
- **Tiny, uneven catalog:** 20 songs, with lofi the most common genre and almost every other genre appearing once, so results are sensitive to which songs happen to exist.
- **No lyrics or instrumental data:** I sometimes want pure instrumentals, but nothing in the data represents that.
- **Self-built profile:** my example profile's targets came from songs in the catalog, so it will naturally rank those songs well. That shows the math works, not that the profile reflects real taste.

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



