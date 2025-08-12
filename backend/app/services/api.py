from typing import Dict, Any
from requests import Session, RequestException
from fastapi import HTTPException
from core.config import settings

class NewsAPIClient:
    """Low-level HTTP client to interact with NewsAPI."""
    def __init__(self, api_key: str, base_url: str = settings.NEWSAPI_BASE_URL, timeout: int = settings.HTTP_TIMEOUT) -> None:
        if not api_key:
            raise RuntimeError("NEWSAPI_KEY is missing. Set it in your environment or .env file.")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = Session()
        self.session.headers.update({"X-Api-Key": self.api_key})

    def _get(self, path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        try:
            resp = self.session.get(url, params=params, timeout=self.timeout)
        except RequestException as e:
            raise HTTPException(status_code=502, detail=f"Upstream connection error: {e}")

        if resp.status_code != 200:
            try:
                payload = resp.json()
                message = payload.get("message") or payload
            except Exception:
                message = resp.text
            raise HTTPException(status_code=resp.status_code, detail=f"NewsAPI error: {message}")

        data = resp.json()
        if data.get("status") != "ok":
            raise HTTPException(status_code=502, detail=f"NewsAPI returned non-ok status: {data}")
        return data

    def get_top_headlines(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self._get("/top-headlines", params)

    def get_everything(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self._get("/everything", params)

    def get_sources(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self._get("/top-headlines/sources", params)


class NewsService:
    """Service layer that orchestrates query building and validations."""
    def __init__(self, client: NewsAPIClient) -> None:
        self.client = client

    def top_headlines(self, query: Dict[str, Any]) -> Dict[str, Any]:
        params = {k: v for k, v in query.items() if v is not None}
        if "sources" in params and (params.get("country") or params.get("category")):
            raise HTTPException(status_code=400, detail="You cannot mix 'sources' with 'country' or 'category'.")
        return self.client.get_top_headlines(params)

    def everything(self, query: Dict[str, Any]) -> Dict[str, Any]:
        if "from_param" in query:
            query["from"] = query.pop("from_param")
        params = {k: v for k, v in query.items() if v is not None}
        return self.client.get_everything(params)

    def sources(self, query: Dict[str, Any]) -> Dict[str, Any]:
        params = {k: v for k, v in query.items() if v is not None}
        return self.client.get_sources(params)
