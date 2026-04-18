# 🎵 Music Recommender Simulation

## Project Summary

For this project I built a small music recommender system that scores songs based on what a user actually likes — their favorite genre, their mood preference, how high-energy they want the music to be, and whether they prefer acoustic or electronic sounds. 
It takes a user profile, runs every song in the catalog through a scoring formula, and returns the top matches ranked highest to lowest. 
The whole thing is content-based,t looks at the song's attributes directly instead of needing data from other users.

---

## How The System Works

### What each song stores

Each song has 10 fields but I only use 4 of them to score it:

- `genre` — like pop, rock, lofi, classical
- `mood` — like happy, intense, chill, sad
- `energy` — a number from 0 to 1 (0.14 is basically a lullaby, 0.94 is a workout song)
- `acousticness` — a number from 0 to 1 (high = guitar/piano, low = electronic/produced)

I dropped tempo and danceability because they were pretty much already covered by energy and mood.

### What the user profile stores

The user profile has four things that match directly to those song features:

- `favorite_genre` — like `"rock"`
- `favorite_mood` — like `"intense"`
- `target_energy` — like `0.85`
- `likes_acoustic` — `True` or `False`

### Algorithm Recipe

For every song, I calculate a score using this formula:

```
score = (genre_match  × 2.0)
      + (mood_match   × 1.5)
      + (1 - |song.energy - target_energy|) × 1.5
      + (acousticness_fit × 1.0)
```

Breaking it down:

1. **Genre match** — if the song's genre matches what you said you like, add 2.0. If not, add nothing. It gets the highest weight because genre is usually the first thing people care about.
2. **Mood match** — same idea but worth 1.5. Matches what you're trying to feel right now.
3. **Energy closeness** — the closer the song's energy is to your target, the more points it gets. So if you want 0.85 energy and the song is 0.91, that's almost perfect. Worth 1.5.
4. **Acousticness fit** — if you like acoustic and the song is acoustic (or vice versa), add 1.0. Worth the least because it's just a yes/no preference.

After every song gets a score, they get sorted from highest to lowest and the top results get returned.

**Example with a rock/intense user:**

| Song | Score |
|---|---|
| Storm Runner (rock, intense, energy 0.91) | **5.91** |
| Midnight Coding (lofi, chill, energy 0.42) | **0.86** |

The system clearly picks Storm Runner — that's the point.

### Possible biases I noticed

- Genre is worth the most points, so a decent rock song will usually beat a really good jazz song if the user said they like rock. That feels a little unfair.
- Mood is all-or-nothing. "Happy" and "nostalgic" get treated like they're totally different even though they're kind of similar.
- My dataset has way more chill and happy songs than sad or angry ones, so users with those preferences get fewer good matches — not because of the formula, just because of what songs exist.

### Terminal Output

Running `python3 -m src.main` with the default pop/happy profile:

![Terminal output showing top 5 recommendations with scores and reasons](https://i.imgur.com/e6kKS89.png)

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


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

