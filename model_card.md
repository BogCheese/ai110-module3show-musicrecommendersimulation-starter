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

**Algorithmic approach, in plain language**

Think of the recommender as a judge who gives every song in the catalog a grade out of 9, then hands you the five songs with the best grades.

To grade a song, the judge compares it with a "taste profile": the mood you want, how upbeat or gloomy you want it to feel, how energetic, how acoustic, and your favorite genre. Each of those is worth a different number of points:

- **Mood: up to 3 points.** This counts most because mood is how I naturally describe a vibe. An exact match earns all 3 points. A similar mood still earns most of them, so "chill" and "relaxed" count as close cousins, while a mood from a neighboring group earns a little and an unrelated one earns nothing.
- **Valence (how happy or gloomy the song sounds): up to 2 points.**
- **Energy (calm to intense): up to 2 points.**
- **Acousticness (soft and organic vs. electronic): up to 1 point.**
- **Genre: up to 1 point,** only for an exact match. It counts least because the catalog is small and most genres appear only once.

For the three number-based features, the judge rewards being close to what you asked for, not being higher or lower. If you want calm music, a song with energy 0.30 earns nearly full points and a song with energy 0.93 earns very few. Added together, the points make the song's grade.

After every song has a grade, the judge puts them in order from highest to lowest. If two songs tie, the one with the closer mood wins, and after that the title decides alphabetically. The top five are shown along with the reasons behind each grade, such as "mood match: sad (+3.0)", so you can see why a song was picked.

**What changed from the starter logic:** the starter suggested a simple recipe of +2.0 for a genre match, +1.0 for a mood match, and a similarity bonus for energy. I made mood count for more than genre, added valence and acousticness as extra features, and let similar moods earn partial credit. Everything is a soft score with no hard filters, so a song that misses on one feature can still rank well overall.

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

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

One weakness I found is that the mood label can outweigh everything else when a profile has conflicting preferences. In my "Sad Banger" test (mood sad, energy 0.9, acousticness 0.1), the system ranked Rainy Window Letters first with 5.93 points, even though it is a quiet acoustic folk song with energy 0.30. It won almost entirely on its exact mood match (3.0 of 9 points), while Ashes in the Static, a loud, dark, non-acoustic metal song that fits the numeric targets far better, scored only 4.72 because its mood is "angry". Doubling the energy weight did not fix this, since the top result was still a medium-energy song (energy 0.45), so the problem is how much the mood label counts, not any single feature. The catalog also has no song that is both sad and high-energy, so listeners whose tastes combine moods and energy levels in unusual ways get recommendations that match only half of what they asked for.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

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
