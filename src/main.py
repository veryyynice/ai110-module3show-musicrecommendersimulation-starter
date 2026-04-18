from src.recommender import load_songs, recommend_songs


PROFILES = {
    # --- Standard profiles ---
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.9,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.91,
        "likes_acoustic": False,
    },
    # --- Adversarial / edge case profiles ---
    "Conflicting: high energy + sad mood": {
        # Energy says gym session, mood says heartbreak — which signal wins?
        "genre": "r&b",
        "mood": "sad",
        "energy": 0.9,
        "likes_acoustic": False,
    },
    "Genre not in catalog (metal)": {
        # genre_match fires for nothing — system must rank purely on energy/mood/acousticness
        "genre": "metal",
        "mood": "intense",
        "energy": 0.91,
        "likes_acoustic": False,
    },
    "Perfect middle energy (0.5)": {
        # 0.5 energy is equidistant from everything — no song feels close, no song feels far
        "genre": "ambient",
        "mood": "peaceful",
        "energy": 0.5,
        "likes_acoustic": True,
    },
    "Acoustic + high energy contradiction": {
        # likes_acoustic=True usually means quiet/soft; high energy usually means electronic
        # forces the system to pick between two signals that rarely coexist in the dataset
        "genre": "folk",
        "mood": "melancholic",
        "energy": 0.88,
        "likes_acoustic": True,
    },
}


def print_results(label: str, songs, recommendations) -> None:
    print(f"\n{'=' * 70}")
    print(f"  Profile: {label}")
    print(f"{'=' * 70}")
    print(f"{'#':<3} {'Title':<25} {'Score':<7} Reasons")
    print("-" * 70)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{i:<3} {song['title']:<25} {score:<7.2f} {explanation}")


def main() -> None:
    songs = load_songs("data/songs.csv")

    for label, prefs in PROFILES.items():
        results = recommend_songs(prefs, songs, k=5)
        print_results(label, songs, results)


if __name__ == "__main__":
    main()
