from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations for pop/happy listener:\n")
    print(f"{'#':<3} {'Title':<25} {'Score':<7} Reasons")
    print("-" * 70)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{i:<3} {song['title']:<25} {score:<7.2f} {explanation}")


if __name__ == "__main__":
    main()
