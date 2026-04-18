import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs ranked by score for the given user."""
        return sorted(self.songs, key=lambda song: self._score(user, song), reverse=True)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable string explaining why this song was recommended."""
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append("genre match (+2.0)")
        if song.mood == user.favorite_mood:
            reasons.append("mood match (+1.5)")
        energy_pts = (1 - abs(song.energy - user.target_energy)) * 1.5
        reasons.append(f"energy closeness (+{energy_pts:.2f})")
        if user.likes_acoustic and song.acousticness > 0.6:
            reasons.append("acousticness fit (+1.0)")
        elif not user.likes_acoustic and song.acousticness < 0.4:
            reasons.append("acousticness fit (+1.0)")
        return ", ".join(reasons)

    def _score(self, user: UserProfile, song: Song) -> float:
        """Compute the weighted score for one song against a user profile."""
        score = 0.0
        if song.genre == user.favorite_genre:
            score += 2.0
        if song.mood == user.favorite_mood:
            score += 1.5
        score += (1 - abs(song.energy - user.target_energy)) * 1.5
        if user.likes_acoustic and song.acousticness > 0.6:
            score += 1.0
        elif not user.likes_acoustic and song.acousticness < 0.4:
            score += 1.0
        return score


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields converted to float/int."""
    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"]           = int(row["id"])
            row["energy"]       = float(row["energy"])
            row["tempo_bpm"]    = float(row["tempo_bpm"])
            row["valence"]      = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences; returns (score, list of reason strings)."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre", ""):
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song["mood"] == user_prefs.get("mood", ""):
        score += 1.5
        reasons.append("mood match (+1.5)")

    target = user_prefs.get("energy", 0.5)
    energy_pts = (1 - abs(song["energy"] - target)) * 1.5
    score += energy_pts
    reasons.append(f"energy closeness (+{energy_pts:.2f})")

    likes_acoustic = user_prefs.get("likes_acoustic", False)
    if likes_acoustic and song["acousticness"] > 0.6:
        score += 1.0
        reasons.append("acousticness fit (+1.0)")
    elif not likes_acoustic and song["acousticness"] < 0.4:
        score += 1.0
        reasons.append("acousticness fit (+1.0)")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs and return the top k as (song, score, explanation) tuples, highest first."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, ", ".join(reasons)))

    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
