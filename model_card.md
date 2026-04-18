# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

---

## 2. Intended Use

VibeMatch is a simple music recommender that suggests songs based on what kind of music someone is in the mood for right now. You give it your favorite genre, your current mood, how energetic you want the music to feel, and whether you prefer acoustic or electronic sounds — and it gives you a ranked list of songs from the catalog that best match those preferences.

This is a classroom simulation, not a real product. It assumes the user knows what they want and can describe it in those four categories. It doesn't learn from you over time and it doesn't track what you've already listened to.

---

## 3. How the Model Works

Every song in the catalog has four things measured about it: its genre, its mood, how energetic it is on a scale from 0 to 1, and how acoustic it sounds on the same scale. When you create a user profile, you're basically saying "here's what I want those four things to be."

The model goes through every song one at a time and gives it a score based on how well it matches. Genre is worth the most points because it's usually the strongest signal for what someone actually wants. Mood is worth slightly less. Energy is scored based on how close the song is to your target — not just yes or no, but how far off it is. Acousticness is worth the least and it's just a yes or no match based on whether you said you like acoustic music.

Once every song has a score, they get sorted from highest to lowest and the top results are returned.

---

## 4. Data

The catalog has 18 songs stored in a CSV file. I started with the 10 songs that came with the project and added 8 more to cover genres and moods that were missing.

**Genres in the catalog:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, classical, r&b, country, edm, folk, soul, latin

**Moods in the catalog:** happy, chill, intense, relaxed, moody, focused, nostalgic, peaceful, romantic, sad, angry, melancholic

The original 10 songs were pretty skewed toward chill and happy vibes. The ones I added help cover more emotional range, but the catalog is still tiny — 18 songs is nothing compared to real streaming platforms. Also, the data reflects a pretty mainstream Western taste. There's no K-pop, no Afrobeats, no regional genres at all.

---

## 5. Strengths

The system works best when the user's preferences are specific and well-represented in the catalog. The clearest example from my testing was the "Deep Intense Rock" profile — Storm Runner hit a perfect score of 6.0 because every single feature matched exactly. The results felt completely right.

It also works well when genre and mood agree with each other. Chill Lofi and High-Energy Pop both gave results that made intuitive sense. The "reasons" output makes it really transparent — you can see exactly why each song was picked, which is something even Spotify doesn't show you.

---

## 6. Limitations and Bias

**Genre dominates too much.** Genre is worth 2.0 points, which means a genre match alone can beat a song that perfectly matches your mood, energy, and acousticness preferences. When I tested a "high energy + sad mood" r&b profile, a romantic r&b song with totally the wrong energy won #1 just because the genre matched.

**Missing genres break the system silently.** If you ask for a genre that doesn't exist in the catalog — like "metal" — genre match never fires for anything. The max possible score drops from 6.0 to 4.0 and the system just gets quietly less accurate. It doesn't tell you anything went wrong.

**Conflicting preferences aren't handled.** Someone who wants high energy but also likes acoustic music is asking for something that barely exists in the dataset. Those two signals fight each other and whoever wins is basically arbitrary. I tested this and a quiet folk song scored 5.0 for a user who said they wanted high-energy music, which is clearly wrong.

**Mood categories are too rigid.** "Sad" and "melancholic" are basically the same feeling but the system treats them as completely unrelated. Same with "happy" and "nostalgic." If your mood isn't an exact match in the catalog, you get zero points for mood.

**Underrepresented moods.** Even with my additions, some moods like "angry" and "sad" only have one or two songs. Those users will always get weak results in positions 3-5.

---

## 7. Evaluation

I tested 7 user profiles total — 3 normal ones and 4 designed to stress or break the system.

The 3 normal profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock) all worked exactly as I expected. Storm Runner hit 6.0, Library Rain hit 5.96, the top results made sense.

The adversarial profiles showed real problems:

- **Conflicting energy + mood** — genre weight pulled in a wrong-vibe song at #1
- **Genre not in catalog** — system degraded silently, scores got closer together
- **Middle energy (0.5)** — every song got a mediocre energy score, results felt almost random
- **Acoustic + high energy** — three features outvoted one, and the system confidently recommended the wrong thing

I also ran the two pytest unit tests that came with the project and they both pass.

---

## 8. Future Work

The biggest thing I'd fix is the genre fallback. If the user's genre isn't in the catalog, the system should probably say so or switch to a "closest genre" mode instead of just silently getting worse.

I'd also want to make mood scoring continuous instead of binary. Something like a similarity table where "sad" and "melancholic" are 80% similar instead of 0% similar would make the results much more forgiving for users whose exact mood isn't in the catalog.

Adding more songs would help a lot too. 18 is not enough to give meaningfully different results for different users — a lot of profiles ended up sharing the same songs in the bottom half of their top 5.

Longer term, it would be cool to add a "don't recommend this again" feature, or weight songs lower if you've already gotten them as a recommendation recently.

---

## 9. Personal Reflection

The biggest thing I learned is that the weights in a scoring formula aren't neutral — they're choices that affect real outcomes. When I set genre to 2.0 and mood to 1.5, I was deciding that genre matters more than mood. That seems reasonable, but the stress tests showed it can backfire when genre and mood disagree. Someone could get recommendations that feel totally off and not know why.

The thing that surprised me most was how confident the system sounds even when it's wrong. When the acoustic + high energy profile returned Autumn Letters at #1 with a score of 5.0, that looks like a great result. But the song is completely wrong for what the user described. Real recommenders probably have this problem too — they show you a confident ranking and you trust it, but the underlying logic might be making weird tradeoffs you can't see.
