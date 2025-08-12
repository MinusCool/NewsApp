from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import news, auth, bookmarks
from database.dtb import init_db


app = FastAPI(
    title="News App Backend (NewsAPI)",
    description="Menyusul",
    version="0.0.0"
)
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok"}

app.include_router(news.router)
app.include_router(auth.router)
app.include_router(bookmarks.router)
