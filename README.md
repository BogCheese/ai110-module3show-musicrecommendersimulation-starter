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

Output of `python -m src.main`, which runs every profile in `PROFILES` (`Loaded songs: 20`). Each block below is the unedited top 5 for one profile. The last four are adversarial profiles built to test the scoring.

#### High-Energy Pop

```
================================================================
 HIGH-ENERGY POP: TOP 5 RECOMMENDATIONS
 Profile: genre pop, mood happy, energy 0.85, valence 0.8, acousticness 0.15
================================================================

#1  Sunrise City - Neon Echo
    pop | happy
    Score: 8.83 / 9.0
    Why:
      - mood match: happy (+3.0)
      - valence close: 0.84 vs target 0.80 (+1.9)
      - energy close: 0.82 vs target 0.85 (+1.9)
      - acousticness close: 0.18 vs target 0.15 (+1.0)
      - genre match: pop (+1.0)
----------------------------------------------------------------

#2  Rooftop Lights - Indigo Parade
    indie pop | happy
    Score: 7.60 / 9.0
    Why:
      - mood match: happy (+3.0)
      - valence close: 0.81 vs target 0.80 (+2.0)
      - energy close: 0.76 vs target 0.85 (+1.8)
      - acousticness close: 0.35 vs target 0.15 (+0.8)
----------------------------------------------------------------

#3  Cumbia Sunset - La Marea
    latin | festive
    Score: 6.97 / 9.0
    Why:
      - similar mood: festive ~ happy (+2.4)
      - valence close: 0.90 vs target 0.80 (+1.8)
      - energy close: 0.80 vs target 0.85 (+1.9)
      - acousticness close: 0.28 vs target 0.15 (+0.9)
----------------------------------------------------------------

#4  Bass Cathedral - Voltage Saints
    edm | euphoric
    Score: 6.91 / 9.0
    Why:
      - similar mood: euphoric ~ happy (+2.4)
      - valence close: 0.88 vs target 0.80 (+1.8)
      - energy close: 0.96 vs target 0.85 (+1.8)
      - acousticness close: 0.04 vs target 0.15 (+0.9)
----------------------------------------------------------------

#5  Gym Hero - Max Pulse
    pop | intense
    Score: 6.58 / 9.0
    Why:
      - similar mood: intense ~ happy (+0.9)
      - valence close: 0.77 vs target 0.80 (+1.9)
      - energy close: 0.93 vs target 0.85 (+1.8)
      - acousticness close: 0.05 vs target 0.15 (+0.9)
      - genre match: pop (+1.0)
----------------------------------------------------------------
```

#### Chill Lofi

```
================================================================
 CHILL LOFI: TOP 5 RECOMMENDATIONS
 Profile: genre lofi, mood chill, energy 0.38, valence 0.58, acousticness 0.8
================================================================

#1  Library Rain - Paper Lanterns
    lofi | chill
    Score: 8.84 / 9.0
    Why:
      - mood match: chill (+3.0)
      - valence close: 0.60 vs target 0.58 (+2.0)
      - energy close: 0.35 vs target 0.38 (+1.9)
      - acousticness close: 0.86 vs target 0.80 (+0.9)
      - genre match: lofi (+1.0)
----------------------------------------------------------------

#2  Midnight Coding - LoRoom
    lofi | chill
    Score: 8.79 / 9.0
    Why:
      - mood match: chill (+3.0)
      - valence close: 0.56 vs target 0.58 (+2.0)
      - energy close: 0.42 vs target 0.38 (+1.9)
      - acousticness close: 0.71 vs target 0.80 (+0.9)
      - genre match: lofi (+1.0)
----------------------------------------------------------------

#3  Focus Flow - LoRoom
    lofi | focused
    Score: 8.32 / 9.0
    Why:
      - similar mood: focused ~ chill (+2.4)
      - valence close: 0.59 vs target 0.58 (+2.0)
      - energy close: 0.40 vs target 0.38 (+2.0)
      - acousticness close: 0.78 vs target 0.80 (+1.0)
      - genre match: lofi (+1.0)
----------------------------------------------------------------

#4  Spacewalk Thoughts - Orbit Bloom
    ambient | chill
    Score: 7.54 / 9.0
    Why:
      - mood match: chill (+3.0)
      - valence close: 0.65 vs target 0.58 (+1.9)
      - energy close: 0.28 vs target 0.38 (+1.8)
      - acousticness close: 0.92 vs target 0.80 (+0.9)
----------------------------------------------------------------

#5  Coffee Shop Stories - Slow Stereo
    jazz | relaxed
    Score: 7.03 / 9.0
    Why:
      - similar mood: relaxed ~ chill (+2.4)
      - valence close: 0.71 vs target 0.58 (+1.7)
      - energy close: 0.37 vs target 0.38 (+2.0)
      - acousticness close: 0.89 vs target 0.80 (+0.9)
----------------------------------------------------------------
```

#### Deep Intense Rock

```
================================================================
 DEEP INTENSE ROCK: TOP 5 RECOMMENDATIONS
 Profile: genre rock, mood intense, energy 0.92, valence 0.45, acousticness 0.08
================================================================

#1  Storm Runner - Voltline
    rock | intense
    Score: 8.90 / 9.0
    Why:
      - mood match: intense (+3.0)
      - valence close: 0.48 vs target 0.45 (+1.9)
      - energy close: 0.91 vs target 0.92 (+2.0)
      - acousticness close: 0.10 vs target 0.08 (+1.0)
      - genre match: rock (+1.0)
----------------------------------------------------------------

#2  Gym Hero - Max Pulse
    pop | intense
    Score: 7.31 / 9.0
    Why:
      - mood match: intense (+3.0)
      - valence close: 0.77 vs target 0.45 (+1.4)
      - energy close: 0.93 vs target 0.92 (+2.0)
      - acousticness close: 0.05 vs target 0.08 (+1.0)
----------------------------------------------------------------

#3  Ashes in the Static - Iron Verdict
    metal | angry
    Score: 6.88 / 9.0
    Why:
      - similar mood: angry ~ intense (+2.4)
      - valence close: 0.25 vs target 0.45 (+1.6)
      - energy close: 0.97 vs target 0.92 (+1.9)
      - acousticness close: 0.06 vs target 0.08 (+1.0)
----------------------------------------------------------------

#4  Concrete Crown - Kid Meridian
    hip hop | confident
    Score: 6.74 / 9.0
    Why:
      - similar mood: confident ~ intense (+2.4)
      - valence close: 0.62 vs target 0.45 (+1.7)
      - energy close: 0.78 vs target 0.92 (+1.7)
      - acousticness close: 0.12 vs target 0.08 (+1.0)
----------------------------------------------------------------

#5  Bass Cathedral - Voltage Saints
    edm | euphoric
    Score: 4.92 / 9.0
    Why:
      - similar mood: euphoric ~ intense (+0.9)
      - valence close: 0.88 vs target 0.45 (+1.1)
      - energy close: 0.96 vs target 0.92 (+1.9)
      - acousticness close: 0.04 vs target 0.08 (+1.0)
----------------------------------------------------------------
```

#### Rainy Day

```
================================================================
 RAINY DAY: TOP 5 RECOMMENDATIONS
 Profile: genre folk, mood sad, energy 0.3, valence 0.25, acousticness 0.85
================================================================

#1  Rainy Window Letters - Hollow Pines
    folk | sad
    Score: 8.86 / 9.0
    Why:
      - mood match: sad (+3.0)
      - valence close: 0.22 vs target 0.25 (+1.9)
      - energy close: 0.30 vs target 0.30 (+2.0)
      - acousticness close: 0.93 vs target 0.85 (+0.9)
      - genre match: folk (+1.0)
----------------------------------------------------------------

#2  Moonlit Sonata Redux - Elena Voss
    classical | melancholic
    Score: 7.04 / 9.0
    Why:
      - similar mood: melancholic ~ sad (+2.4)
      - valence close: 0.30 vs target 0.25 (+1.9)
      - energy close: 0.22 vs target 0.30 (+1.8)
      - acousticness close: 0.95 vs target 0.85 (+0.9)
----------------------------------------------------------------

#3  Smoke and Neon Blues - Delta Marlowe
    blues | bittersweet
    Score: 6.86 / 9.0
    Why:
      - similar mood: bittersweet ~ sad (+2.4)
      - valence close: 0.28 vs target 0.25 (+1.9)
      - energy close: 0.45 vs target 0.30 (+1.7)
      - acousticness close: 0.67 vs target 0.85 (+0.8)
----------------------------------------------------------------

#4  Library Rain - Paper Lanterns
    lofi | chill
    Score: 5.09 / 9.0
    Why:
      - similar mood: chill ~ sad (+0.9)
      - valence close: 0.60 vs target 0.25 (+1.3)
      - energy close: 0.35 vs target 0.30 (+1.9)
      - acousticness close: 0.86 vs target 0.85 (+1.0)
----------------------------------------------------------------

#5  Spacewalk Thoughts - Orbit Bloom
    ambient | chill
    Score: 4.99 / 9.0
    Why:
      - similar mood: chill ~ sad (+0.9)
      - valence close: 0.65 vs target 0.25 (+1.2)
      - energy close: 0.28 vs target 0.30 (+2.0)
      - acousticness close: 0.92 vs target 0.85 (+0.9)
----------------------------------------------------------------
```

#### Sad Banger (conflicting)

```
================================================================
 SAD BANGER (CONFLICTING): TOP 5 RECOMMENDATIONS
 Profile: genre pop, mood sad, energy 0.9, valence 0.2, acousticness 0.1
================================================================

#1  Rainy Window Letters - Hollow Pines
    folk | sad
    Score: 5.93 / 9.0
    Why:
      - mood match: sad (+3.0)
      - valence close: 0.22 vs target 0.20 (+2.0)
      - energy close: 0.30 vs target 0.90 (+0.8)
      - acousticness close: 0.93 vs target 0.10 (+0.2)
----------------------------------------------------------------

#2  Smoke and Neon Blues - Delta Marlowe
    blues | bittersweet
    Score: 5.77 / 9.0
    Why:
      - similar mood: bittersweet ~ sad (+2.4)
      - valence close: 0.28 vs target 0.20 (+1.8)
      - energy close: 0.45 vs target 0.90 (+1.1)
      - acousticness close: 0.67 vs target 0.10 (+0.4)
----------------------------------------------------------------

#3  Moonlit Sonata Redux - Elena Voss
    classical | melancholic
    Score: 4.99 / 9.0
    Why:
      - similar mood: melancholic ~ sad (+2.4)
      - valence close: 0.30 vs target 0.20 (+1.8)
      - energy close: 0.22 vs target 0.90 (+0.6)
      - acousticness close: 0.95 vs target 0.10 (+0.2)
----------------------------------------------------------------

#4  Gym Hero - Max Pulse
    pop | intense
    Score: 4.75 / 9.0
    Why:
      - valence close: 0.77 vs target 0.20 (+0.9)
      - energy close: 0.93 vs target 0.90 (+1.9)
      - acousticness close: 0.05 vs target 0.10 (+0.9)
      - genre match: pop (+1.0)
----------------------------------------------------------------

#5  Ashes in the Static - Iron Verdict
    metal | angry
    Score: 4.72 / 9.0
    Why:
      - valence close: 0.25 vs target 0.20 (+1.9)
      - energy close: 0.97 vs target 0.90 (+1.9)
      - acousticness close: 0.06 vs target 0.10 (+1.0)
----------------------------------------------------------------
```

#### Genre Trap (lofi but intense)

```
================================================================
 GENRE TRAP (LOFI BUT INTENSE): TOP 5 RECOMMENDATIONS
 Profile: genre lofi, mood intense, energy 0.95, valence 0.5, acousticness 0.05
================================================================

#1  Storm Runner - Voltline
    rock | intense
    Score: 7.83 / 9.0
    Why:
      - mood match: intense (+3.0)
      - valence close: 0.48 vs target 0.50 (+2.0)
      - energy close: 0.91 vs target 0.95 (+1.9)
      - acousticness close: 0.10 vs target 0.05 (+0.9)
----------------------------------------------------------------

#2  Gym Hero - Max Pulse
    pop | intense
    Score: 7.42 / 9.0
    Why:
      - mood match: intense (+3.0)
      - valence close: 0.77 vs target 0.50 (+1.5)
      - energy close: 0.93 vs target 0.95 (+2.0)
      - acousticness close: 0.05 vs target 0.05 (+1.0)
----------------------------------------------------------------

#3  Ashes in the Static - Iron Verdict
    metal | angry
    Score: 6.85 / 9.0
    Why:
      - similar mood: angry ~ intense (+2.4)
      - valence close: 0.25 vs target 0.50 (+1.5)
      - energy close: 0.97 vs target 0.95 (+2.0)
      - acousticness close: 0.06 vs target 0.05 (+1.0)
----------------------------------------------------------------

#4  Concrete Crown - Kid Meridian
    hip hop | confident
    Score: 6.75 / 9.0
    Why:
      - similar mood: confident ~ intense (+2.4)
      - valence close: 0.62 vs target 0.50 (+1.8)
      - energy close: 0.78 vs target 0.95 (+1.7)
      - acousticness close: 0.12 vs target 0.05 (+0.9)
----------------------------------------------------------------

#5  Bass Cathedral - Voltage Saints
    edm | euphoric
    Score: 5.11 / 9.0
    Why:
      - similar mood: euphoric ~ intense (+0.9)
      - valence close: 0.88 vs target 0.50 (+1.2)
      - energy close: 0.96 vs target 0.95 (+2.0)
      - acousticness close: 0.04 vs target 0.05 (+1.0)
----------------------------------------------------------------
```

#### Unknown Mood and Genre

```
================================================================
 UNKNOWN MOOD AND GENRE: TOP 5 RECOMMENDATIONS
 Profile: genre k-pop, mood mysterious, energy 0.6, valence 0.6, acousticness 0.5
================================================================

#1  Dust Road Home - Billy Marrow
    country | nostalgic
    Score: 4.54 / 9.0
    Why:
      - valence close: 0.66 vs target 0.60 (+1.9)
      - energy close: 0.55 vs target 0.60 (+1.9)
      - acousticness close: 0.74 vs target 0.50 (+0.8)
----------------------------------------------------------------

#2  Velvet Hours - Amara Vale
    r&b | romantic
    Score: 4.52 / 9.0
    Why:
      - valence close: 0.68 vs target 0.60 (+1.8)
      - energy close: 0.52 vs target 0.60 (+1.8)
      - acousticness close: 0.34 vs target 0.50 (+0.8)
----------------------------------------------------------------

#3  Midnight Coding - LoRoom
    lofi | chill
    Score: 4.35 / 9.0
    Why:
      - valence close: 0.56 vs target 0.60 (+1.9)
      - energy close: 0.42 vs target 0.60 (+1.6)
      - acousticness close: 0.71 vs target 0.50 (+0.8)
----------------------------------------------------------------

#4  Focus Flow - LoRoom
    lofi | focused
    Score: 4.30 / 9.0
    Why:
      - valence close: 0.59 vs target 0.60 (+2.0)
      - energy close: 0.40 vs target 0.60 (+1.6)
      - acousticness close: 0.78 vs target 0.50 (+0.7)
----------------------------------------------------------------

#5  Island Breeze - Sun Drifters
    reggae | uplifting
    Score: 4.25 / 9.0
    Why:
      - valence close: 0.85 vs target 0.60 (+1.5)
      - energy close: 0.50 vs target 0.60 (+1.8)
      - acousticness close: 0.45 vs target 0.50 (+0.9)
----------------------------------------------------------------
```

#### Dead Center (no mood/genre)

```
================================================================
 DEAD CENTER (NO MOOD/GENRE): TOP 5 RECOMMENDATIONS
 Profile: energy 0.5, valence 0.5, acousticness 0.5
================================================================

#1  Midnight Coding - LoRoom
    lofi | chill
    Score: 4.51 / 5.0
    Why:
      - valence close: 0.56 vs target 0.50 (+1.9)
      - energy close: 0.42 vs target 0.50 (+1.8)
      - acousticness close: 0.71 vs target 0.50 (+0.8)
----------------------------------------------------------------

#2  Velvet Hours - Amara Vale
    r&b | romantic
    Score: 4.44 / 5.0
    Why:
      - valence close: 0.68 vs target 0.50 (+1.6)
      - energy close: 0.52 vs target 0.50 (+2.0)
      - acousticness close: 0.34 vs target 0.50 (+0.8)
----------------------------------------------------------------

#3  Dust Road Home - Billy Marrow
    country | nostalgic
    Score: 4.34 / 5.0
    Why:
      - valence close: 0.66 vs target 0.50 (+1.7)
      - energy close: 0.55 vs target 0.50 (+1.9)
      - acousticness close: 0.74 vs target 0.50 (+0.8)
----------------------------------------------------------------

#4  Focus Flow - LoRoom
    lofi | focused
    Score: 4.34 / 5.0
    Why:
      - valence close: 0.59 vs target 0.50 (+1.8)
      - energy close: 0.40 vs target 0.50 (+1.8)
      - acousticness close: 0.78 vs target 0.50 (+0.7)
----------------------------------------------------------------

#5  Smoke and Neon Blues - Delta Marlowe
    blues | bittersweet
    Score: 4.29 / 5.0
    Why:
      - valence close: 0.28 vs target 0.50 (+1.6)
      - energy close: 0.45 vs target 0.50 (+1.9)
      - acousticness close: 0.67 vs target 0.50 (+0.8)
----------------------------------------------------------------
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



