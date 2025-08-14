from pydantic import BaseModel, AnyHttpUrl, Field
from typing import Optional, List, Dict
from datetime import datetime
class RegisterIn(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)

class LoginIn(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class Source(BaseModel):
    id: Optional[str] = None
    name: str

class Article(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    url: AnyHttpUrl
    image_url: Optional[AnyHttpUrl] = None
    source: Source
    author: Optional[str] = None
    published_at: Optional[datetime] = None

class PagedArticles(BaseModel):
    items: List[Article]
    page: int
    page_size: int
    total: int
    total_pages: int
    has_next: bool
    sort: Optional[str] = None

class HomeResponse(BaseModel):
    sections: Dict[str, PagedArticles] 

class BookmarkIn(BaseModel):
    title: str
    url: AnyHttpUrl
    source: Optional[str] = None
    published_at: Optional[datetime] = None
    description: Optional[str] = None
    image_url: Optional[AnyHttpUrl] = None

class BookmarkOut(BaseModel):
    id: int
    title: str
    url: AnyHttpUrl
    source: Optional[str] = None
    published_at: Optional[datetime] = None
    description: Optional[str] = None
    image_url: Optional[AnyHttpUrl] = None
