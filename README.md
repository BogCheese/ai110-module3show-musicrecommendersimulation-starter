# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

**MoodMatch 1.0** is a small, command-line music recommender. It loads a 20-song catalog from `data/songs.csv` and compares every song to a taste profile (mood, valence, energy, acousticness, and genre). It prints the top 5 as a table, with the reasons behind each score. It is content-based only: it uses song attributes and one fixed taste profile, and it has no data about other users. I tested it on 8 profiles, including 4 adversarial ones, and wrote up what I found in the [model card](model_card.md).

---

## How The System Works

Real-world recommenders like Spotify and YouTube work in three steps:

1. **Input data.** They collect user behavior, such as plays, skips, likes, saves, playlists, and listening or watch history. They also collect song features, such as genre, mood, tempo, energy, and lyrics or audio analysis.
2. **User preferences.** From that data, they build a picture of each user's taste. *Collaborative filtering* learns it from people with similar behavior ("listeners like you also played..."). *Content-based filtering* learns it from the features of songs you already liked.
3. **Ranking and selection.** They give every candidate song a score for how well it fits that taste. Then they sort the scores and show only the top few. Large systems also add rules for variety and freshness.

My version is a simplified, purely content-based recommender, and it follows the same three steps:

- **Input data:** the song table in `data/songs.csv` (genre, mood, energy, valence, acousticness, and more).
- **User preferences:** one fixed taste profile with a favorite mood and genre, plus target values for energy, valence, and acousticness. There is no listening history.
- **Ranking and selection:** every song gets a score in points, up to 9.0, that rewards *closeness* to the profile instead of simply higher or lower values. The songs are sorted by score and the top 5 are shown.

I prioritize **mood** most heavily, since that is how I naturally describe a vibe. Next come **valence and energy**, with **acousticness** and **genre** as smaller tie-breakers. Mood uses partial credit so that similar moods such as chill and relaxed still count as a match. Everything is a soft score with no hard filters, so a song that misses on one feature can still rank well overall.

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

**Scoring Rule** (one song vs. the profile, result in points, up to 9.0):

| Component | Weight | How it is computed |
|---|---|---|
| Mood | 3.0 | Partial credit by mood family: exact match 1.0, close mood about 0.8, loosely related 0.3-0.5, unrelated 0 (so chill and relaxed still match) |
| Valence | 2.0 | `1 - abs(song_valence - target_valence)` |
| Energy | 2.0 | `1 - abs(song_energy - target_energy)` |
| Acousticness | 1.0 | `1 - abs(song_acousticness - target_acousticness)` |
| Genre | 1.0 | 1.0 for an exact match, otherwise 0 |

`score = sum(weight x component)`, in raw points with a maximum of 9.0. Each song's reasons list shows the points that add up to its score.

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

Output of `python -m src.main`, which runs every profile in `PROFILES` (`Loaded songs: 20`). Each block below is the unedited top 5 for one profile, shown as a table with the reasons behind every score. The last four profiles are adversarial cases built to test the scoring. A summary table comparing all profiles comes last.

#### High-Energy Pop

```
===========================================================================================
 HIGH-ENERGY POP: TOP 5 RECOMMENDATIONS
 Profile: genre pop, mood happy, energy 0.85, valence 0.8, acousticness 0.15
===========================================================================================
+-----+-------------------+------------+--------------------------------------------------+
|  #  | Song              |   Score    | Reasons                                          |
+=====+===================+============+==================================================+
|  1  | Sunrise City      | 8.83 / 9.0 | - mood match: happy (+3.0)                       |
|     | Neon Echo         |            | - valence close: 0.84 vs target 0.80 (+1.9)      |
|     | pop | happy       |            | - energy close: 0.82 vs target 0.85 (+1.9)       |
|     |                   |            | - acousticness close: 0.18 vs target 0.15 (+1.0) |
|     |                   |            | - genre match: pop (+1.0)                        |
+-----+-------------------+------------+--------------------------------------------------+
|  2  | Rooftop Lights    | 7.60 / 9.0 | - mood match: happy (+3.0)                       |
|     | Indigo Parade     |            | - valence close: 0.81 vs target 0.80 (+2.0)      |
|     | indie pop | happy |            | - energy close: 0.76 vs target 0.85 (+1.8)       |
|     |                   |            | - acousticness close: 0.35 vs target 0.15 (+0.8) |
+-----+-------------------+------------+--------------------------------------------------+
|  3  | Cumbia Sunset     | 6.97 / 9.0 | - similar mood: festive ~ happy (+2.4)           |
|     | La Marea          |            | - valence close: 0.90 vs target 0.80 (+1.8)      |
|     | latin | festive   |            | - energy close: 0.80 vs target 0.85 (+1.9)       |
|     |                   |            | - acousticness close: 0.28 vs target 0.15 (+0.9) |
+-----+-------------------+------------+--------------------------------------------------+
|  4  | Bass Cathedral    | 6.91 / 9.0 | - similar mood: euphoric ~ happy (+2.4)          |
|     | Voltage Saints    |            | - valence close: 0.88 vs target 0.80 (+1.8)      |
|     | edm | euphoric    |            | - energy close: 0.96 vs target 0.85 (+1.8)       |
|     |                   |            | - acousticness close: 0.04 vs target 0.15 (+0.9) |
+-----+-------------------+------------+--------------------------------------------------+
|  5  | Gym Hero          | 6.58 / 9.0 | - similar mood: intense ~ happy (+0.9)           |
|     | Max Pulse         |            | - valence close: 0.77 vs target 0.80 (+1.9)      |
|     | pop | intense     |            | - energy close: 0.93 vs target 0.85 (+1.8)       |
|     |                   |            | - acousticness close: 0.05 vs target 0.15 (+0.9) |
|     |                   |            | - genre match: pop (+1.0)                        |
+-----+-------------------+------------+--------------------------------------------------+
```

#### Chill Lofi

```
=============================================================================================
 CHILL LOFI: TOP 5 RECOMMENDATIONS
 Profile: genre lofi, mood chill, energy 0.38, valence 0.58, acousticness 0.8
=============================================================================================
+-----+---------------------+------------+--------------------------------------------------+
|  #  | Song                |   Score    | Reasons                                          |
+=====+=====================+============+==================================================+
|  1  | Library Rain        | 8.84 / 9.0 | - mood match: chill (+3.0)                       |
|     | Paper Lanterns      |            | - valence close: 0.60 vs target 0.58 (+2.0)      |
|     | lofi | chill        |            | - energy close: 0.35 vs target 0.38 (+1.9)       |
|     |                     |            | - acousticness close: 0.86 vs target 0.80 (+0.9) |
|     |                     |            | - genre match: lofi (+1.0)                       |
+-----+---------------------+------------+--------------------------------------------------+
|  2  | Midnight Coding     | 8.79 / 9.0 | - mood match: chill (+3.0)                       |
|     | LoRoom              |            | - valence close: 0.56 vs target 0.58 (+2.0)      |
|     | lofi | chill        |            | - energy close: 0.42 vs target 0.38 (+1.9)       |
|     |                     |            | - acousticness close: 0.71 vs target 0.80 (+0.9) |
|     |                     |            | - genre match: lofi (+1.0)                       |
+-----+---------------------+------------+--------------------------------------------------+
|  3  | Focus Flow          | 8.32 / 9.0 | - similar mood: focused ~ chill (+2.4)           |
|     | LoRoom              |            | - valence close: 0.59 vs target 0.58 (+2.0)      |
|     | lofi | focused      |            | - energy close: 0.40 vs target 0.38 (+2.0)       |
|     |                     |            | - acousticness close: 0.78 vs target 0.80 (+1.0) |
|     |                     |            | - genre match: lofi (+1.0)                       |
+-----+---------------------+------------+--------------------------------------------------+
|  4  | Spacewalk Thoughts  | 7.54 / 9.0 | - mood match: chill (+3.0)                       |
|     | Orbit Bloom         |            | - valence close: 0.65 vs target 0.58 (+1.9)      |
|     | ambient | chill     |            | - energy close: 0.28 vs target 0.38 (+1.8)       |
|     |                     |            | - acousticness close: 0.92 vs target 0.80 (+0.9) |
+-----+---------------------+------------+--------------------------------------------------+
|  5  | Coffee Shop Stories | 7.03 / 9.0 | - similar mood: relaxed ~ chill (+2.4)           |
|     | Slow Stereo         |            | - valence close: 0.71 vs target 0.58 (+1.7)      |
|     | jazz | relaxed      |            | - energy close: 0.37 vs target 0.38 (+2.0)       |
|     |                     |            | - acousticness close: 0.89 vs target 0.80 (+0.9) |
+-----+---------------------+------------+--------------------------------------------------+
```

#### Deep Intense Rock

```
=============================================================================================
 DEEP INTENSE ROCK: TOP 5 RECOMMENDATIONS
 Profile: genre rock, mood intense, energy 0.92, valence 0.45, acousticness 0.08
=============================================================================================
+-----+---------------------+------------+--------------------------------------------------+
|  #  | Song                |   Score    | Reasons                                          |
+=====+=====================+============+==================================================+
|  1  | Storm Runner        | 8.90 / 9.0 | - mood match: intense (+3.0)                     |
|     | Voltline            |            | - valence close: 0.48 vs target 0.45 (+1.9)      |
|     | rock | intense      |            | - energy close: 0.91 vs target 0.92 (+2.0)       |
|     |                     |            | - acousticness close: 0.10 vs target 0.08 (+1.0) |
|     |                     |            | - genre match: rock (+1.0)                       |
+-----+---------------------+------------+--------------------------------------------------+
|  2  | Gym Hero            | 7.31 / 9.0 | - mood match: intense (+3.0)                     |
|     | Max Pulse           |            | - valence close: 0.77 vs target 0.45 (+1.4)      |
|     | pop | intense       |            | - energy close: 0.93 vs target 0.92 (+2.0)       |
|     |                     |            | - acousticness close: 0.05 vs target 0.08 (+1.0) |
+-----+---------------------+------------+--------------------------------------------------+
|  3  | Ashes in the Static | 6.88 / 9.0 | - similar mood: angry ~ intense (+2.4)           |
|     | Iron Verdict        |            | - valence close: 0.25 vs target 0.45 (+1.6)      |
|     | metal | angry       |            | - energy close: 0.97 vs target 0.92 (+1.9)       |
|     |                     |            | - acousticness close: 0.06 vs target 0.08 (+1.0) |
+-----+---------------------+------------+--------------------------------------------------+
|  4  | Concrete Crown      | 6.74 / 9.0 | - similar mood: confident ~ intense (+2.4)       |
|     | Kid Meridian        |            | - valence close: 0.62 vs target 0.45 (+1.7)      |
|     | hip hop | confident |            | - energy close: 0.78 vs target 0.92 (+1.7)       |
|     |                     |            | - acousticness close: 0.12 vs target 0.08 (+1.0) |
+-----+---------------------+------------+--------------------------------------------------+
|  5  | Bass Cathedral      | 4.92 / 9.0 | - similar mood: euphoric ~ intense (+0.9)        |
|     | Voltage Saints      |            | - valence close: 0.88 vs target 0.45 (+1.1)      |
|     | edm | euphoric      |            | - energy close: 0.96 vs target 0.92 (+1.9)       |
|     |                     |            | - acousticness close: 0.04 vs target 0.08 (+1.0) |
+-----+---------------------+------------+--------------------------------------------------+
```

#### Rainy Day

```
=================================================================================================
 RAINY DAY: TOP 5 RECOMMENDATIONS
 Profile: genre folk, mood sad, energy 0.3, valence 0.25, acousticness 0.85
=================================================================================================
+-----+-------------------------+------------+--------------------------------------------------+
|  #  | Song                    |   Score    | Reasons                                          |
+=====+=========================+============+==================================================+
|  1  | Rainy Window Letters    | 8.86 / 9.0 | - mood match: sad (+3.0)                         |
|     | Hollow Pines            |            | - valence close: 0.22 vs target 0.25 (+1.9)      |
|     | folk | sad              |            | - energy close: 0.30 vs target 0.30 (+2.0)       |
|     |                         |            | - acousticness close: 0.93 vs target 0.85 (+0.9) |
|     |                         |            | - genre match: folk (+1.0)                       |
+-----+-------------------------+------------+--------------------------------------------------+
|  2  | Moonlit Sonata Redux    | 7.04 / 9.0 | - similar mood: melancholic ~ sad (+2.4)         |
|     | Elena Voss              |            | - valence close: 0.30 vs target 0.25 (+1.9)      |
|     | classical | melancholic |            | - energy close: 0.22 vs target 0.30 (+1.8)       |
|     |                         |            | - acousticness close: 0.95 vs target 0.85 (+0.9) |
+-----+-------------------------+------------+--------------------------------------------------+
|  3  | Smoke and Neon Blues    | 6.86 / 9.0 | - similar mood: bittersweet ~ sad (+2.4)         |
|     | Delta Marlowe           |            | - valence close: 0.28 vs target 0.25 (+1.9)      |
|     | blues | bittersweet     |            | - energy close: 0.45 vs target 0.30 (+1.7)       |
|     |                         |            | - acousticness close: 0.67 vs target 0.85 (+0.8) |
+-----+-------------------------+------------+--------------------------------------------------+
|  4  | Library Rain            | 5.09 / 9.0 | - similar mood: chill ~ sad (+0.9)               |
|     | Paper Lanterns          |            | - valence close: 0.60 vs target 0.25 (+1.3)      |
|     | lofi | chill            |            | - energy close: 0.35 vs target 0.30 (+1.9)       |
|     |                         |            | - acousticness close: 0.86 vs target 0.85 (+1.0) |
+-----+-------------------------+------------+--------------------------------------------------+
|  5  | Spacewalk Thoughts      | 4.99 / 9.0 | - similar mood: chill ~ sad (+0.9)               |
|     | Orbit Bloom             |            | - valence close: 0.65 vs target 0.25 (+1.2)      |
|     | ambient | chill         |            | - energy close: 0.28 vs target 0.30 (+2.0)       |
|     |                         |            | - acousticness close: 0.92 vs target 0.85 (+0.9) |
+-----+-------------------------+------------+--------------------------------------------------+
```

#### Sad Banger (conflicting)

```
=================================================================================================
 SAD BANGER (CONFLICTING): TOP 5 RECOMMENDATIONS
 Profile: genre pop, mood sad, energy 0.9, valence 0.2, acousticness 0.1
=================================================================================================
+-----+-------------------------+------------+--------------------------------------------------+
|  #  | Song                    |   Score    | Reasons                                          |
+=====+=========================+============+==================================================+
|  1  | Rainy Window Letters    | 5.93 / 9.0 | - mood match: sad (+3.0)                         |
|     | Hollow Pines            |            | - valence close: 0.22 vs target 0.20 (+2.0)      |
|     | folk | sad              |            | - energy close: 0.30 vs target 0.90 (+0.8)       |
|     |                         |            | - acousticness close: 0.93 vs target 0.10 (+0.2) |
+-----+-------------------------+------------+--------------------------------------------------+
|  2  | Smoke and Neon Blues    | 5.77 / 9.0 | - similar mood: bittersweet ~ sad (+2.4)         |
|     | Delta Marlowe           |            | - valence close: 0.28 vs target 0.20 (+1.8)      |
|     | blues | bittersweet     |            | - energy close: 0.45 vs target 0.90 (+1.1)       |
|     |                         |            | - acousticness close: 0.67 vs target 0.10 (+0.4) |
+-----+-------------------------+------------+--------------------------------------------------+
|  3  | Moonlit Sonata Redux    | 4.99 / 9.0 | - similar mood: melancholic ~ sad (+2.4)         |
|     | Elena Voss              |            | - valence close: 0.30 vs target 0.20 (+1.8)      |
|     | classical | melancholic |            | - energy close: 0.22 vs target 0.90 (+0.6)       |
|     |                         |            | - acousticness close: 0.95 vs target 0.10 (+0.2) |
+-----+-------------------------+------------+--------------------------------------------------+
|  4  | Gym Hero                | 4.75 / 9.0 | - valence close: 0.77 vs target 0.20 (+0.9)      |
|     | Max Pulse               |            | - energy close: 0.93 vs target 0.90 (+1.9)       |
|     | pop | intense           |            | - acousticness close: 0.05 vs target 0.10 (+0.9) |
|     |                         |            | - genre match: pop (+1.0)                        |
+-----+-------------------------+------------+--------------------------------------------------+
|  5  | Ashes in the Static     | 4.72 / 9.0 | - valence close: 0.25 vs target 0.20 (+1.9)      |
|     | Iron Verdict            |            | - energy close: 0.97 vs target 0.90 (+1.9)       |
|     | metal | angry           |            | - acousticness close: 0.06 vs target 0.10 (+1.0) |
+-----+-------------------------+------------+--------------------------------------------------+
```

#### Genre Trap (lofi but intense)

```
=============================================================================================
 GENRE TRAP (LOFI BUT INTENSE): TOP 5 RECOMMENDATIONS
 Profile: genre lofi, mood intense, energy 0.95, valence 0.5, acousticness 0.05
=============================================================================================
+-----+---------------------+------------+--------------------------------------------------+
|  #  | Song                |   Score    | Reasons                                          |
+=====+=====================+============+==================================================+
|  1  | Storm Runner        | 7.83 / 9.0 | - mood match: intense (+3.0)                     |
|     | Voltline            |            | - valence close: 0.48 vs target 0.50 (+2.0)      |
|     | rock | intense      |            | - energy close: 0.91 vs target 0.95 (+1.9)       |
|     |                     |            | - acousticness close: 0.10 vs target 0.05 (+0.9) |
+-----+---------------------+------------+--------------------------------------------------+
|  2  | Gym Hero            | 7.42 / 9.0 | - mood match: intense (+3.0)                     |
|     | Max Pulse           |            | - valence close: 0.77 vs target 0.50 (+1.5)      |
|     | pop | intense       |            | - energy close: 0.93 vs target 0.95 (+2.0)       |
|     |                     |            | - acousticness close: 0.05 vs target 0.05 (+1.0) |
+-----+---------------------+------------+--------------------------------------------------+
|  3  | Ashes in the Static | 6.85 / 9.0 | - similar mood: angry ~ intense (+2.4)           |
|     | Iron Verdict        |            | - valence close: 0.25 vs target 0.50 (+1.5)      |
|     | metal | angry       |            | - energy close: 0.97 vs target 0.95 (+2.0)       |
|     |                     |            | - acousticness close: 0.06 vs target 0.05 (+1.0) |
+-----+---------------------+------------+--------------------------------------------------+
|  4  | Concrete Crown      | 6.75 / 9.0 | - similar mood: confident ~ intense (+2.4)       |
|     | Kid Meridian        |            | - valence close: 0.62 vs target 0.50 (+1.8)      |
|     | hip hop | confident |            | - energy close: 0.78 vs target 0.95 (+1.7)       |
|     |                     |            | - acousticness close: 0.12 vs target 0.05 (+0.9) |
+-----+---------------------+------------+--------------------------------------------------+
|  5  | Bass Cathedral      | 5.11 / 9.0 | - similar mood: euphoric ~ intense (+0.9)        |
|     | Voltage Saints      |            | - valence close: 0.88 vs target 0.50 (+1.2)      |
|     | edm | euphoric      |            | - energy close: 0.96 vs target 0.95 (+2.0)       |
|     |                     |            | - acousticness close: 0.04 vs target 0.05 (+1.0) |
+-----+---------------------+------------+--------------------------------------------------+
```

#### Unknown Mood and Genre

```
=============================================================================================
 UNKNOWN MOOD AND GENRE: TOP 5 RECOMMENDATIONS
 Profile: genre k-pop, mood mysterious, energy 0.6, valence 0.6, acousticness 0.5
=============================================================================================
+-----+---------------------+------------+--------------------------------------------------+
|  #  | Song                |   Score    | Reasons                                          |
+=====+=====================+============+==================================================+
|  1  | Dust Road Home      | 4.54 / 9.0 | - valence close: 0.66 vs target 0.60 (+1.9)      |
|     | Billy Marrow        |            | - energy close: 0.55 vs target 0.60 (+1.9)       |
|     | country | nostalgic |            | - acousticness close: 0.74 vs target 0.50 (+0.8) |
+-----+---------------------+------------+--------------------------------------------------+
|  2  | Velvet Hours        | 4.52 / 9.0 | - valence close: 0.68 vs target 0.60 (+1.8)      |
|     | Amara Vale          |            | - energy close: 0.52 vs target 0.60 (+1.8)       |
|     | r&b | romantic      |            | - acousticness close: 0.34 vs target 0.50 (+0.8) |
+-----+---------------------+------------+--------------------------------------------------+
|  3  | Midnight Coding     | 4.35 / 9.0 | - valence close: 0.56 vs target 0.60 (+1.9)      |
|     | LoRoom              |            | - energy close: 0.42 vs target 0.60 (+1.6)       |
|     | lofi | chill        |            | - acousticness close: 0.71 vs target 0.50 (+0.8) |
+-----+---------------------+------------+--------------------------------------------------+
|  4  | Focus Flow          | 4.30 / 9.0 | - valence close: 0.59 vs target 0.60 (+2.0)      |
|     | LoRoom              |            | - energy close: 0.40 vs target 0.60 (+1.6)       |
|     | lofi | focused      |            | - acousticness close: 0.78 vs target 0.50 (+0.7) |
+-----+---------------------+------------+--------------------------------------------------+
|  5  | Island Breeze       | 4.25 / 9.0 | - valence close: 0.85 vs target 0.60 (+1.5)      |
|     | Sun Drifters        |            | - energy close: 0.50 vs target 0.60 (+1.8)       |
|     | reggae | uplifting  |            | - acousticness close: 0.45 vs target 0.50 (+0.9) |
+-----+---------------------+------------+--------------------------------------------------+
```

#### Dead Center (no mood/genre)

```
==============================================================================================
 DEAD CENTER (NO MOOD/GENRE): TOP 5 RECOMMENDATIONS
 Profile: energy 0.5, valence 0.5, acousticness 0.5
==============================================================================================
+-----+----------------------+------------+--------------------------------------------------+
|  #  | Song                 |   Score    | Reasons                                          |
+=====+======================+============+==================================================+
|  1  | Midnight Coding      | 4.51 / 5.0 | - valence close: 0.56 vs target 0.50 (+1.9)      |
|     | LoRoom               |            | - energy close: 0.42 vs target 0.50 (+1.8)       |
|     | lofi | chill         |            | - acousticness close: 0.71 vs target 0.50 (+0.8) |
+-----+----------------------+------------+--------------------------------------------------+
|  2  | Velvet Hours         | 4.44 / 5.0 | - valence close: 0.68 vs target 0.50 (+1.6)      |
|     | Amara Vale           |            | - energy close: 0.52 vs target 0.50 (+2.0)       |
|     | r&b | romantic       |            | - acousticness close: 0.34 vs target 0.50 (+0.8) |
+-----+----------------------+------------+--------------------------------------------------+
|  3  | Dust Road Home       | 4.34 / 5.0 | - valence close: 0.66 vs target 0.50 (+1.7)      |
|     | Billy Marrow         |            | - energy close: 0.55 vs target 0.50 (+1.9)       |
|     | country | nostalgic  |            | - acousticness close: 0.74 vs target 0.50 (+0.8) |
+-----+----------------------+------------+--------------------------------------------------+
|  4  | Focus Flow           | 4.34 / 5.0 | - valence close: 0.59 vs target 0.50 (+1.8)      |
|     | LoRoom               |            | - energy close: 0.40 vs target 0.50 (+1.8)       |
|     | lofi | focused       |            | - acousticness close: 0.78 vs target 0.50 (+0.7) |
+-----+----------------------+------------+--------------------------------------------------+
|  5  | Smoke and Neon Blues | 4.29 / 5.0 | - valence close: 0.28 vs target 0.50 (+1.6)      |
|     | Delta Marlowe        |            | - energy close: 0.45 vs target 0.50 (+1.9)       |
|     | blues | bittersweet  |            | - acousticness close: 0.67 vs target 0.50 (+0.8) |
+-----+----------------------+------------+--------------------------------------------------+
```

#### Summary of all profiles

```
=========================================================================================================
 SUMMARY OF ALL PROFILES
=========================================================================================================
+-------------------------------+----------------------+------------+----------------------+------------+
| Profile                       | Top pick             |   Score    | Runner-up            |   Score    |
+===============================+======================+============+======================+============+
| High-Energy Pop               | Sunrise City         | 8.83 / 9.0 | Rooftop Lights       | 7.60 / 9.0 |
+-------------------------------+----------------------+------------+----------------------+------------+
| Chill Lofi                    | Library Rain         | 8.84 / 9.0 | Midnight Coding      | 8.79 / 9.0 |
+-------------------------------+----------------------+------------+----------------------+------------+
| Deep Intense Rock             | Storm Runner         | 8.90 / 9.0 | Gym Hero             | 7.31 / 9.0 |
+-------------------------------+----------------------+------------+----------------------+------------+
| Rainy Day                     | Rainy Window Letters | 8.86 / 9.0 | Moonlit Sonata Redux | 7.04 / 9.0 |
+-------------------------------+----------------------+------------+----------------------+------------+
| Sad Banger (conflicting)      | Rainy Window Letters | 5.93 / 9.0 | Smoke and Neon Blues | 5.77 / 9.0 |
+-------------------------------+----------------------+------------+----------------------+------------+
| Genre Trap (lofi but intense) | Storm Runner         | 7.83 / 9.0 | Gym Hero             | 7.42 / 9.0 |
+-------------------------------+----------------------+------------+----------------------+------------+
| Unknown Mood and Genre        | Dust Road Home       | 4.54 / 9.0 | Velvet Hours         | 4.52 / 9.0 |
+-------------------------------+----------------------+------------+----------------------+------------+
| Dead Center (no mood/genre)   | Midnight Coding      | 4.51 / 5.0 | Velvet Hours         | 4.44 / 5.0 |
+-------------------------------+----------------------+------------+----------------------+------------+
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

### Experiment 1: change the weights (energy x2, genre x0.5)

I doubled the energy weight (2.0 to 4.0) and halved the genre weight (1.0 to 0.5), then re-ran all 8 profiles. I checked that every score stayed between 0 and the profile's maximum, and that a perfect match scored the new maximum of 10.5.

- **5 of 8 profiles kept the exact same order.** Scores went up only because more points were available.
- **Sad Banger changed.** Rainy Window Letters fell from #1 to #2. Smoke and Neon Blues took #1, and Ashes in the Static rose from #5 to #3.
- **Unknown Mood and Genre and Dead Center shuffled** among near-ties, which were already close to noise.
- **Verdict: different, not clearly more accurate.** The #1 song for Sad Banger was still a medium-energy song, and its top 5 scores squeezed into a 0.68-point range. I changed the weights back.

### Experiment 2: different types of users

I ran 8 profiles: 4 everyday tastes (High-Energy Pop, Chill Lofi, Deep Intense Rock, Rainy Day) and 4 adversarial ones (Sad Banger, Genre Trap, Unknown Mood and Genre, Dead Center). The full output is in "Sample Recommendation Output" above, and the pair-by-pair comparisons are in the [model card](model_card.md). Opposite tastes got opposite lists, and the Genre Trap profile could not pull lofi songs into a loud, intense list.

### Smaller changes

- I moved "nostalgic" from the sad-like mood family to the calm family. Dust Road Home dropped out of the Rainy Day top 5, because sharing a family with "sad" gave it too much credit.
- I show each score out of that profile's own maximum, so Dead Center reads 4.51 / 5.0 instead of a misleading 4.51 / 9.0.

---

## Limitations and Risks

- **Tiny catalog.** It has only 20 songs, and 15 of the 17 genres appear once.
- **The mood label can outweigh everything else.** In the Sad Banger test, a quiet folk song beat a loud metal song because of one mood match.
- **Energy and acousticness move together** in this data (correlation of -0.96), so unusual tastes, like loud acoustic music, get penalized twice.
- **Some moods have no family.** "Romantic" and "moody" earn mood points only from an exact match.
- **It does not understand lyrics, language, or whether a song is instrumental.**
- **One fixed taste per user.** It cannot handle "sad songs to code, loud songs at the gym".
- **It never says "nothing fits".** It always returns five songs, even when every score is low.

The model card goes deeper on these: [Model Card](model_card.md).

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

A recommender turns data into predictions by comparing. Each song is a row of labels and numbers. The user is another row of target values. The score says how close the two rows are, and sorting the scores gives the list. My version does not learn anything, but its lists still felt like taste, and the reasons next to each score made it easy to see why a song was picked.

Bias can show up in three places. The first is the data: with 20 songs, a listener whose taste has no good match still gets five songs with no warning. The second is the weights, which are my opinions. I decided mood counts for 3 points, and the Sad Banger test showed that one mood label can beat a better numeric fit. The third is the assumptions: one fixed taste per person, and mood groups I drew by hand. A real app would repeat these problems on millions of users, so the people with unusual tastes would be served worst.



