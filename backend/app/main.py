from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import news, auth, bookmarks
from database.migrate import init_db
from core.config import settings


app = FastAPI(
    title="News App Backend (NewsAPI)",
    description="Menyusul",
    version="0.0.0"
)

allowed = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(news.router)
app.include_router(auth.router)
app.include_router(bookmarks.router)

init_db()

@app.get("/")
def read_root():
    return {"status": "ok"}
