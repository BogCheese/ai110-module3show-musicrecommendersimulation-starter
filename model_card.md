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

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

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
