"""
Reddit Public JSON Scraper 
"""

import httpx
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
import random

from utils.decorators import timed, retry

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

BASE_URL = "https://www.reddit.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Cache-Control": "max-age=0",
}


class RedditScraper:
    def __init__(self, timeout: float = 15.0):
        self.timeout = timeout
        self.client = None
        self._initialized = False

    async def _ensure_client(self):
        if not self._initialized:
            self.client = httpx.AsyncClient(
                headers=HEADERS,
                timeout=self.timeout,
                follow_redirects=True,
            )
            self._initialized = True

    @retry(max_attempts=2, delay=2)
    @timed
    async def _get(self, url: str, params: dict = None) -> dict:
        await self._ensure_client()

        try:
            await asyncio.sleep(random.uniform(0.5, 1.5))

            response = await self.client.get(url, params=params)

            if response.status_code != 200:
                print(f"[ERROR] {response.status_code} for {url}")
                return {}

            return response.json()

        except Exception as e:
            print(f"[REQUEST ERROR] {e}")
            return {}

    @timed
    async def search_posts(self, query: str, limit: int = 25) -> List[Dict]:
        url = f"{BASE_URL}/search.json"
        params = {
            "q": query,
            "limit": min(limit, 50),
            "sort": "relevance",
            "t": "month"
        }

        data = await self._get(url, params)
        posts = self._parse_posts(data)

        if not posts:
            params = {"q": query, "limit": min(limit, 25)}
            data = await self._get(url, params)
            posts = self._parse_posts(data)

        return posts

    @timed
    async def get_subreddit_posts(self, subreddit: str, limit: int = 25) -> List[Dict]:
        urls = [
            f"{BASE_URL}/r/{subreddit}/hot.json",
            f"{BASE_URL}/r/{subreddit}/new.json",
            f"{BASE_URL}/r/{subreddit}.json"
        ]

        for url in urls:
            params = {"limit": min(limit, 25)}
            data = await self._get(url, params)
            posts = self._parse_posts(data, subreddit=subreddit)

            if posts:
                return posts

        return []

    def _parse_posts(self, data: dict, subreddit: Optional[str] = None) -> List[Dict]:
        posts = []

        if not data:
            return posts

        children = data.get("data", {}).get("children", [])

        for child in children:
            d = child.get("data", {})

            title = d.get("title", "")
            body = d.get("selftext", "")

            text = title
            if body and body not in ["[removed]", "[deleted]", ""]:
                text += " " + body

            if not text.strip():
                continue

            posts.append({
                "id": d.get("id"),
                "title": title,
                "text": text,
                "score": d.get("score", 0),
                "subreddit": d.get("subreddit", subreddit),
                "author": d.get("author", "unknown"),
                "created_utc": datetime.fromtimestamp(
                    d.get("created_utc", 0)
                ).isoformat(),
                "url": "https://reddit.com" + d.get("permalink", ""),
                "num_comments": d.get("num_comments", 0)
            })

        return posts

    async def close(self):
        if self.client and self._initialized:
            await self.client.aclose()
            self._initialized = False