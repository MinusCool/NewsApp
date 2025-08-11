from typing import Optional, List
from pydantic import BaseModel, Field

class TopHeadlinesQuery(BaseModel):
    country: Optional[str] = Field(default=None, description="2-letter ISO 3166-1 code, e.g., 'us', 'gb'")
    category: Optional[str] = Field(default=None, description="business, entertainment, general, health, science, sports, technology")
    sources: Optional[str] = Field(default=None, description="comma-separated source ids (can't mix with country/category)")
    q: Optional[str] = Field(default=None, description="Keywords or phrases to search for")
    pageSize: int = Field(default=20, ge=1, le=100)
    page: int = Field(default=1, ge=1)

class EverythingQuery(BaseModel):
    q: Optional[str] = None
    qInTitle: Optional[str] = None
    sources: Optional[str] = None
    domains: Optional[str] = None
    excludeDomains: Optional[str] = None
    from_param: Optional[str] = Field(default=None, alias="from")
    to: Optional[str] = None
    language: Optional[str] = None
    sortBy: Optional[str] = Field(default=None, description="relevancy, popularity, publishedAt")
    pageSize: int = Field(default=20, ge=1, le=100)
    page: int = Field(default=1, ge=1)

class SourcesQuery(BaseModel):
    category: Optional[str] = None
    language: Optional[str] = None
    country: Optional[str] = None

class NewsResponse(BaseModel):
    status: str
    totalResults: Optional[int] = None
    articles: Optional[list] = None
    sources: Optional[list] = None

class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

class BookmarkIn(BaseModel):
    title: str
    url: str
    source: Optional[str] = None
    published_at: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None

class BookmarkOut(BookmarkIn):
    id: int