"""
API routes for sentiment analysis.
"""

from collections import Counter
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query

from scraping.reddit_scraper import RedditScraper
from ml.model_loader import ModelLoader
from ml.predictor import Predictor

router = APIRouter()

# =========================================================
# Load ML model at startup
# =========================================================

predictor = None

try:
    BASE_DIR = Path(__file__).resolve().parent.parent

    model_path = BASE_DIR / "models" / "best_model.pkl"
    vectorizer_path = BASE_DIR / "models" / "vectorizer.pkl"

    print("[INFO] Loading machine learning model...")

    loader = ModelLoader(
        model_path=str(model_path),
        vectorizer_path=str(vectorizer_path)
    )

    predictor = Predictor(
        loader.get_model(),
        loader.get_vectorizer()
    )

    print("[INFO] Model loaded successfully.")

except Exception as e:
    print(f"[ERROR] Failed to load model: {e}")


# =========================================================
# Analyze Endpoint
# =========================================================

@router.get("/analyze")
async def analyze(
    query: str = Query(..., min_length=1),
    limit: int = Query(30, ge=5, le=50)
):
    """
    Analyze Reddit posts sentiment based on a search query.
    """

    if predictor is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded"
        )

    scraper = RedditScraper()

    try:
        # Search Reddit posts
        posts = await scraper.search_posts(query, limit)

        if not posts:
            return {
                "query": query,
                "count": 0,
                "results": [],
                "message": "No posts found"
            }

        # Find top subreddits
        subreddit_counter = Counter(
            p["subreddit"] for p in posts if p.get("subreddit")
        )

        top_subreddits = [
            s for s, _ in subreddit_counter.most_common(3)
        ]

        # Collect additional posts
        extra_posts = []

        for subreddit in top_subreddits:
            try:
                subreddit_posts = await scraper.get_subreddit_posts(
                    subreddit,
                    limit=10
                )
                extra_posts.extend(subreddit_posts)

            except Exception as e:
                print(f"[WARNING] Failed subreddit fetch: {e}")

        all_posts = posts + extra_posts

        # Run batch prediction
        texts = [p["text"] for p in all_posts]

        predictions = predictor.predict_batch(texts)

        results = []
        sentiments = []

        for post, prediction in zip(all_posts, predictions):

            sentiment = prediction["sentiment"]
            confidence = prediction["confidence"]

            sentiments.append(sentiment)

            results.append({
                "title": post.get("title"),
                "text": post.get("text")[:500],
                "score": post.get("score"),
                "subreddit": post.get("subreddit"),
                "url": post.get("url"),
                "sentiment": sentiment,
                "confidence": confidence
            })

        # Sentiment statistics
        total = len(sentiments)
        counts = Counter(sentiments)

        summary = {
            "positive_pct": round(
                counts.get("Positive", 0) / total * 100, 1
            ),
            "negative_pct": round(
                counts.get("Negative", 0) / total * 100, 1
            ),
            "neutral_pct": round(
                counts.get("Neutral", 0) / total * 100, 1
            ),
        }

        return {
            "query": query,
            "count": len(results),
            "summary": summary,
            "results": results,
            "top_subreddits": top_subreddits
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        await scraper.close()


# =========================================================
# Health Check Endpoint
# =========================================================

@router.get("/health")
async def health_check():
    """
    Check API health status.
    """
    return {
        "status": "healthy",
        "model_loaded": predictor is not None
    }