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

Default pop/happy profile:

![Terminal output showing top 5 recommendations with scores and reasons](https://i.imgur.com/e6kKS89.png)

All 7 profiles run against the 18-song catalog:

![Terminal output showing all profile recommendations with scores and reasons](https://i.imgur.com/9ZsLOkv.png)

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

I ran 7 profiles total — 3 normal ones and 4 designed to break or stress the system.

**Normal profiles (worked as expected):**

| Profile | #1 Result | Score | Why it made sense |
|---|---|---|---|
| High-Energy Pop | Sunrise City | 5.88 | genre + mood + energy + acousticness all matched |
| Chill Lofi | Library Rain | 5.96 | same — all 4 features fired |
| Deep Intense Rock | Storm Runner | 6.00 | perfect score, every feature matched exactly |

**Adversarial profiles (where things got weird):**

**"Conflicting: high energy + sad mood" (r&b, sad, energy 0.9)**
The #1 result was Still Waters — an r&b song with romantic mood and energy 0.54. It won because genre matched (+2.0) even though its energy was way off and the mood wasn't sad at all. This showed that genre weight is strong enough to pull in a totally wrong song if the genre happens to match.

**"Genre not in catalog (metal)"**
When the genre doesn't exist in the dataset, genre_match never fires for anything. The max possible score dropped from 6.0 to 4.0 and the system basically became an energy + mood matcher. Storm Runner still came out first, which was fine, but the gap between songs got way smaller and the results felt less confident.

**"Perfect middle energy (0.5)"**
With target energy right in the middle, every song gets a mediocre energy score — nothing feels close, nothing feels far. Genre ended up being the only real separator. The results felt almost random for songs without a genre match.

**"Acoustic + high energy contradiction" (folk, melancholic, energy 0.88)**
This one was the most interesting failure. Autumn Letters (folk, melancholic, energy 0.21) won with a score of 5.0 even though its energy was completely wrong. Genre + mood + acousticness all matched and basically outvoted the energy penalty. The system recommended a quiet folk song to someone who said they wanted high energy music, which is a real problem.

---

## Limitations and Risks

- **Genre outweighs everything** — a genre match adds 2.0 points, which can override a bad mood and bad energy match combined. If the catalog has your genre but only one song in it, you're getting that song no matter what.
- **Missing genre = broken experience** — if you type a genre that's not in the dataset (like "metal"), genre_match never fires and the whole system gets less accurate. There's no fallback.
- **Contradictory preferences aren't handled** — if someone wants high energy but also likes acoustic, those two signals fight each other because high-energy songs are almost always low-acousticness. The system just picks whoever wins the point battle, which isn't actually what the user wants.
- **Mood is binary and too strict** — "sad" and "melancholic" get treated as completely different even though they're basically the same vibe. Same with "happy" vs "nostalgic." Real feelings don't have hard edges like that.
- **Tiny catalog** — 18 songs isn't enough to give different users meaningfully different results. A lot of profiles end up with the same songs in positions 3-5.
- **No listening history** — the system doesn't know if you already heard a song 50 times and are sick of it.

---

## Reflection

[**Model Card**](model_card.md)
