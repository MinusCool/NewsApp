from fastapi import APIRouter, Depends
from models.schemas import TopHeadlinesQuery, EverythingQuery, SourcesQuery, NewsResponse
from services.api import NewsAPIClient, NewsService
from core.config import settings

router = APIRouter(prefix="/news", tags=["news"])

def get_service() -> NewsService:
    client = NewsAPIClient(api_key=settings.NEWSAPI_KEY)
    return NewsService(client)

@router.get("/top-headlines", response_model=NewsResponse)
def top_headlines(params: TopHeadlinesQuery = Depends(), svc: NewsService = Depends(get_service)):
    return svc.top_headlines(params.dict(by_alias=True))

@router.get("/everything", response_model=NewsResponse)
def everything(params: EverythingQuery = Depends(), svc: NewsService = Depends(get_service)):
    return svc.everything(params.dict(by_alias=True))

@router.get("/sources", response_model=NewsResponse)
def sources(params: SourcesQuery = Depends(), svc: NewsService = Depends(get_service)):
    return svc.sources(params.dict(by_alias=True))
