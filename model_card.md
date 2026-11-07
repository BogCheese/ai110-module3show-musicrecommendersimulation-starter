# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**MoodMatch 1.0**

A small recommender that picks songs by mood first.

---

## 2. Goal / Task and Intended Use

**Goal.** MoodMatch suggests songs a person might like next. It reads one taste profile. It scores every song in a small catalog. Then it shows the top 5, with reasons.

**What it assumes about the user.**

- Each user has one fixed taste.
- The user can describe that taste with a mood, a genre, and a few numbers.
- Songs that sound close to the profile will feel right.

**Intended use.**

- Classroom learning about how recommenders work.
- Trying ideas, like changing weights, on a tiny catalog.
- Showing why each song was picked.

**Not intended for.**

- Real music apps or real listeners. The catalog is far too small.
- Guessing how a person feels, or judging their mental health, from the mood they pick.
- Deciding which artists get exposure or money.
- People who want very different music at different times, like sad songs to code and loud songs at the gym.
- Treating a score as proof that a song is good.

---

## 3. Algorithm Summary (How the Model Works)

Think of the system as a judge. The judge gives every song a grade. Then it picks the best five.

The judge compares each song to your taste profile. Each feature is worth some points:

- **Mood: up to 3 points.** An exact match gets all 3. A similar mood, like chill and relaxed, gets most of them. A neighboring mood gets a little. An unrelated mood gets none.
- **Valence: up to 2 points.** This is how happy or gloomy a song sounds.
- **Energy: up to 2 points.** This is calm to intense.
- **Acousticness: up to 1 point.** This is soft and organic vs. electronic.
- **Genre: up to 1 point.** Only an exact match counts.

For the number features, closer is better. Higher or lower does not matter. Say you want calm music. A song with energy 0.30 earns almost full points. A song with energy 0.93 earns very few.

The points add up to the song's grade. The most a song can get is 9. It is less if a profile skips mood or genre.

Then the songs are sorted from best to worst. If two songs tie, the closer mood wins. After that, the title decides. The top 5 are shown with their reasons, like "mood match: sad (+3.0)".

**Why mood counts most.** Mood is how I describe a vibe. Genre is a weak signal here, because most genres have only one song.

**What I changed from the starter.** The starter suggested +2 for genre, +1 for mood, and an energy bonus. I made mood count more than genre. I added valence and acousticness. I let similar moods earn partial credit. Everything is a soft score. There are no hard filters.

---

## 4. Data Used

- The catalog has **20 songs**. The starter had 10. I added 10 more.
- Each song has a title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness.
- The numbers run from 0 to 1. Tempo is in beats per minute.
- There are 17 genres and 16 moods.
- I wrote the values for my 10 songs by hand. They are plausible, but they are not measured from real audio.
- The scorer uses mood, valence, energy, acousticness, and genre. It loads tempo and danceability but does not score them.

**Limits of the data.**

- It is tiny. 15 of the 17 genres have only one song.
- Lofi is the most common genre, with 3 songs.
- Only 3 songs have middle energy. 8 are calm and 9 are loud.
- Energy and acousticness move together. Loud songs are electronic. Calm songs are acoustic.
- There is no lyrics, language, instrumental, or popularity data.

---

## 5. Strengths

- Clear profiles get sensible results. Pop gets Sunrise City. Lofi gets Library Rain. Rock gets Storm Runner.
- Opposite tastes get opposite lists. Rock and Rainy Day share no songs.
- Every pick comes with reasons. It is easy to see why a song ranked where it did.
- Similar moods count. Chill and relaxed songs still score well for each other.
- It is steady. When I doubled energy and halved genre, 5 of 8 profiles kept the same order.
- Genre cannot trick it. Genre Trap asked for lofi but wanted loud music. No lofi song appeared.

---

## 6. Observed Behavior / Biases (Limitations)

**Main weakness.**

One weakness I found is that the mood label can outweigh everything else when a profile has conflicting preferences. In my "Sad Banger" test (mood sad, energy 0.9, acousticness 0.1), the system ranked Rainy Window Letters first with 5.93 points, even though it is a quiet acoustic folk song with energy 0.30. It won almost entirely on its exact mood match (3.0 of 9 points), while Ashes in the Static, a loud, dark, non-acoustic metal song that fits the numeric targets far better, scored only 4.72 because its mood is "angry". Doubling the energy weight did not fix this, since the top result was still a medium-energy song (energy 0.45), so the problem is how much the mood label counts, not any single feature. The catalog also has no song that is both sad and high-energy, so listeners whose tastes combine moods and energy levels in unusual ways get recommendations that match only half of what they asked for.

**Other patterns I saw.**

- Energy and acousticness move together in this catalog (correlation of -0.96). No song is loud and acoustic. No song is calm and electronic. The score counts both, so unusual tastes get penalized twice.
- "Romantic" and "moody" belong to no mood family. They only earn mood points from an exact match. A romantic listener gets one great song (8.46). The next best is about 4.6.
- Few songs have middle energy. Profiles that asked for the middle got flat, noisy lists. The top 5 scores were less than 0.3 points apart.
- Gym Hero shows up in 4 of the 8 top-5 lists. A loud, fairly upbeat song sits close to many tastes.
- The system never says "nothing here fits". It always returns five songs.

---

## 7. Evaluation Process

**Short version.**

- I tested 8 taste profiles: 4 everyday tastes and 4 tricky ones.
- I read each top 5 list and checked if it matched the vibe.
- I ran one experiment: energy doubled, genre halved. Then I changed it back.
- I compared profiles in pairs. I also explained why Gym Hero keeps showing up.
- The only automated tests are the two starter tests. I judged the scoring by reading the results, not with a metric.

**Details**

**Profiles I tested**

I ran eight taste profiles through the recommender and read the top 5 for each, checking whether the songs matched how I would describe that vibe.

- **Four everyday tastes:** High-Energy Pop, Chill Lofi, Deep Intense Rock, and Rainy Day (sad, calm, acoustic).
- **Four "try to trick it" profiles:** Sad Banger (sad mood but very high energy), Genre Trap (loves lofi, but wants loud intense music), Unknown Mood and Genre (asks for a mood and genre that no song has), and Dead Center (every number set to the middle, no mood or genre).

I also ran one experiment: doubling the importance of energy and halving genre. Five of the eight profiles kept exactly the same order, so the system is fairly steady when a profile is clear. Only the conflicting and vague profiles moved. I changed the weights back afterward.

**What surprised me**

- **Genre Trap did not get tricked.** The profile says "lofi", but no lofi song appears in its top 5. Genre is only worth 1 point out of 9, so loud songs won because everything else about the profile asked for loud songs.
- **Sad Banger gave a quiet folk song as its first pick.** The person asked for high energy, but the mood label "sad" was worth so many points that a calm acoustic song beat a loud, dark metal song.
- **The vague profiles were basically a coin flip.** For Unknown Mood and Genre, the top 5 scores were only 0.29 points apart. When a profile has no strong preferences, the system has no real reason to prefer one song over another, and it does not tell the user that.
- **Some first places were nearly ties.** For Chill Lofi, Library Rain beat Midnight Coding by 0.05 points, which is not a meaningful difference.

**Comparing pairs of profiles**

I did not compare all 28 possible pairs. These pairs cover every profile at least once.

- **High-Energy Pop vs. Chill Lofi:** The pop list is loud and bright (Sunrise City, Rooftop Lights, Cumbia Sunset), and the lofi list is quiet and soft (Library Rain, Midnight Coding, Focus Flow). Not one song appears in both lists. This makes sense because the two profiles sit at opposite ends of energy and acousticness, so the scoring pushes them to opposite ends of the catalog.
- **Chill Lofi vs. Rainy Day:** Both want calm, acoustic music, so they share songs such as Library Rain and Spacewalk Thoughts. The difference is mood: Rainy Day puts the gloomy songs first (Rainy Window Letters, Moonlit Sonata Redux, Smoke and Neon Blues), and Chill Lofi puts the relaxed ones first. This is the right result, since the main difference between these two listeners is how sad they want to feel.
- **High-Energy Pop vs. Deep Intense Rock:** Both want loud songs, so Gym Hero and Bass Cathedral show up in both. What separates them is mood and valence. Pop leads with happy songs, and Rock leads with Storm Runner and the darker, angrier songs. That fits: they want the same loudness but a different feeling.
- **Deep Intense Rock vs. Genre Trap:** These two get the exact same five songs in the same order (Storm Runner, Gym Hero, Ashes in the Static, Concrete Crown, Bass Cathedral), though the scores differ a little. The only real difference is that Genre Trap says "lofi" instead of "rock", and that changed no rankings. This shows that a genre match is a small bonus here, not a deciding factor, which is what I intended.
- **Rainy Day vs. Sad Banger:** Both ask for a sad mood, but Sad Banger also asks for loud music. The sad songs still rank near the top for both, but Sad Banger pulls in loud songs lower down (Gym Hero, Ashes in the Static) that Rainy Day never shows. The scores for Sad Banger are also much lower (5.93 at the top vs. 8.86), which correctly signals that no song fits the whole request.
- **Deep Intense Rock vs. Rainy Day:** These are opposites. Rock gets loud songs with low acousticness, and Rainy Day gets quiet, acoustic ones, with no overlap in their top picks. This is the clearest sign that the energy and acousticness settings work.
- **Unknown Mood and Genre vs. Dead Center:** Both lists are made of middle-of-the-road songs (Dust Road Home, Velvet Hours, Midnight Coding), with almost the same songs in a slightly different order. This makes sense, because with no mood or genre match available, only the middle-range numbers can decide, and both profiles ask for the middle. It also shows the weakness: when nothing stands out, the order is close to random.

**Why does "Gym Hero" keep showing up for people who just want Happy Pop?**

The system matches songs against a checklist, and Gym Hero ticks almost every box for a Happy Pop fan. It is a pop song. It is loud, upbeat, and bright, which is close to the energy and positivity the profile asked for. The only box it misses is the mood label: Gym Hero is tagged "intense", not "happy". But the system treats "intense" as a close neighbor of "happy", since both are high-energy moods, so it still gives partial credit. That is enough to put it in 5th place for Happy Pop, with 6.58 out of 9. It never wins, because the truly happy songs score higher.

The same thing happens in four of my eight profiles, because a loud song that sounds fairly positive is close to a lot of different tastes, and the catalog only has 20 songs. A real listener would say that workout music and happy music feel different, even if both are loud. The system cannot tell the difference between "cheerful" and "pumped up" beyond that one mood label, which is a real limit of this simple design.

---

## 8. Ideas for Improvement

1. **Make mood count less.** Try 2 points instead of 3. Or cap how much a mood label can win. Then re-run Sad Banger and see if the loud, dark songs rise.
2. **Add better data.** Add more songs, with more per genre. Add loud acoustic songs and calm electronic songs. Add an instrumental column, since I sometimes want music without lyrics.
3. **Handle more than one taste.** Let a user have contexts, like "coding" and "gym". Also warn when no song fits well, and keep one song like Gym Hero from crowding the lists.

---

## 9. Personal Reflection

**Biggest learning moment.** A recommender is a set of opinions written as math. I picked every weight myself. Mood got 3 points and genre got 1. That sounded fine until I tried "Sad Banger". A quiet folk song beat a loud metal song because of one mood label. Doubling the energy weight did not fix it. That showed me the weights decide who gets good results.

**How AI helped, and when I double-checked it.** AI helped me plan the scoring, write the code, run the profiles, and spot patterns, like energy and acousticness moving together. But I could not trust it blindly. Here is what I had to check:

- The starter `main.py` had an import that crashed with `python -m src.main`. It had to be fixed.
- One score looked fine at first. Dead Center showed 4.51 out of 9, which reads like 50%. The real maximum for that profile was 5, so it was really a 90% match.
- A claim that two profiles had "almost the same" lists was wrong. The lists were identical.
- The mood groups, like putting "nostalgic" with "calm", were judgment calls. I made those calls, not the AI.

I learned to run the code and compare it to the claim before believing a summary.

**What surprised me.** Simple math can feel like taste. The system does not learn anything. It only adds up points for how close each song is. But the Rainy Day list felt right. The reasons, like "mood match: sad (+3.0)", made it feel smart, even though the system has no idea what sad music feels like. Gym Hero showed me the limit. The system cannot tell "cheerful" from "pumped up".

**What I would try next.** I want a real screen instead of the terminal. The terminal output is messy to read. I would like a clean page that updates as I change things. My idea is a simple app with sliders for energy, valence, and acousticness, and dropdowns for mood and genre. The top 5 songs would update live, with the reasons shown next to each one. The project already lists Streamlit in `requirements.txt`, so that is a natural place to start. I would also add a way to switch between my saved profiles, like Rainy Day and Chill Lofi, and compare them side by side.
