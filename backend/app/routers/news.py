from fastapi import APIRouter, Query
from typing import Optional, Literal
from models.schemas import PagedArticles, HomeResponse
from services.api import NewsAPI

router = APIRouter(prefix="/news", tags=["news"])
svc = NewsAPI()

@router.get("/search", response_model=PagedArticles)
def search(
    q: str,
    sources: Optional[str] = None,
    language: Optional[str] = None,
    from_: Optional[str] = Query(None, alias="from"),
    to: Optional[str] = None,
    sort: Literal["relevancy","popularity","publishedAt"] = "publishedAt",
    page: int = 1,
    page_size: int = 20,
):
    return svc.search(q=q, sources=sources, language=language, from_=from_, to=to, sort=sort, page=page, page_size=page_size)

@router.get("/top", response_model=PagedArticles)
def top(
    country: Optional[str] = "id",
    category: Optional[str] = None,
    sources: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
):
    return svc.top(country=country, category=category, sources=sources, page=page, page_size=page_size)

@router.get("/home", response_model=HomeResponse)
def home():
    return {"sections": svc.home_sections()}

@router.get("/sources")
def sources(category: Optional[str] = None, language: Optional[str] = None, country: Optional[str] = None):
    return svc.sources(category=category, language=language, country=country)
