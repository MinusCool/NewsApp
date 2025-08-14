from typing import Optional, Literal, Dict, Any, Tuple
import requests, time, hashlib
from fastapi import HTTPException, status
from core.config import settings

class TTLCache:
    def __init__(self, ttl_seconds: int = 180, max_items: int = 32):
        self.ttl = ttl_seconds
        self.max = max_items
        self.data: Dict[str, Tuple[float, Any]] = {}

    def get(self, key: str):
        now = time.time()
        v = self.data.get(key)
        if not v:
            return None
        t, obj = v
        if now - t > self.ttl:
            self.data.pop(key, None)
            return None
        return obj

    def set(self, key: str, value: Any):
        if len(self.data) >= self.max:
            oldest = sorted(self.data.items(), key=lambda kv: kv[1][0])[0][0]
            self.data.pop(oldest, None)
        self.data[key] = (time.time(), value)

cache = TTLCache(ttl_seconds=180, max_items=32)
class NewsAPI:
    def __init__(self):
        self.base = settings.NEWSAPI_BASE_URL.rstrip("/")
        self.key = settings.NEWSAPI_KEY
        self.timeout = settings.HTTP_TIMEOUT
        self.session = requests.Session()
        self.session.headers.update({"X-Api-Key": self.key})

    def _request(self, path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            r = self.session.get(f"{self.base}/{path.lstrip('/')}", params=params, timeout=self.timeout)
        except requests.RequestException as e:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Upstream error") from e
        if r.status_code != 200:
            try:
                data = r.json()
                msg = data.get("message") or "Upstream non-200"
            except Exception:
                msg = "Upstream non-200"
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=msg)
        return r.json()

    @staticmethod
    def _aid(url: str) -> str:
        import hashlib
        return hashlib.sha1(url.encode("utf-8")).hexdigest()

    @staticmethod
    def _normalize_article(a: Dict[str, Any]):
        title = a.get("title")
        url = a.get("url")
        if not title or not url:
            return None
        return {
            "id": NewsAPI._aid(url),
            "title": title,
            "description": a.get("description"),
            "url": url,
            "image_url": a.get("urlToImage"),
            "source": {"id": (a.get("source") or {}).get("id"), "name": (a.get("source") or {}).get("name")},
            "author": a.get("author"),
            "published_at": a.get("publishedAt"),
        }

    @staticmethod
    def _envelope(items, page: int, page_size: int, total: int, sort: Optional[str] = None):
        total_pages = max(1, (total + page_size - 1) // page_size)
        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "sort": sort,
        }

    def search(self, *, q: str, sources: Optional[str], language: Optional[str],
               from_: Optional[str], to: Optional[str],
               sort: Literal["relevancy","popularity","publishedAt"], page: int, page_size: int):
        params = {"q": q, "page": page, "pageSize": page_size, "sortBy": sort}
        if sources: params["sources"] = sources
        if language: params["language"] = language
        if from_: params["from"] = from_
        if to: params["to"] = to
        data = self._request("everything", params)
        raw = data.get("articles", [])
        total = data.get("totalResults", 0)
        items = [x for x in (self._normalize_article(a) for a in raw) if x]
        return self._envelope(items, page, page_size, total, sort)

    def top(self, *, country: Optional[str], category: Optional[str], sources: Optional[str],
            page: int, page_size: int):
        if sources and (country or category):
            raise HTTPException(status_code=400, detail="sources cannot be mixed with country/category")
        params = {"page": page, "pageSize": page_size}
        if country: params["country"] = country
        if category: params["category"] = category
        if sources: params["sources"] = sources
        data = self._request("top-headlines", params)
        raw = data.get("articles", [])
        total = data.get("totalResults", 0)
        items = [x for x in (self._normalize_article(a) for a in raw) if x]
        return self._envelope(items, page, page_size, total, None)

    def sources(self, *, category: Optional[str], language: Optional[str], country: Optional[str]):
        params = {}
        if category: params["category"] = category
        if language: params["language"] = language
        if country: params["country"] = country
        return self._request("top-headlines/sources", params)

    def home_sections(self):
        key = "home_sections_v1"
        cached = cache.get(key)
        if cached:
            return cached
        sections = {
            "top": self.top(country="id", category=None, sources=None, page=1, page_size=10),
            "technology": self.top(country="id", category="technology", sources=None, page=1, page_size=10),
            "business": self.top(country="id", category="business", sources=None, page=1, page_size=10),
            "sports": self.top(country="id", category="sports", sources=None, page=1, page_size=10),
        }
        cache.set(key, sections)
        return sections