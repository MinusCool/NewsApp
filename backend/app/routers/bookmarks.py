from fastapi import APIRouter, HTTPException, Query
from typing import List
from models.schemas import BookmarkIn, BookmarkOut
from repositories.bookmarkRepo import BookmarkRepository
from repositories.userRepo import UserRepository

router = APIRouter(prefix="/bookmarks", tags=["bookmarks"])
_bookmarks = BookmarkRepository()
_users = UserRepository()

def _ensure_user(user_id: int):
    if not _users.get_user_by_id(user_id):
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/", response_model=List[BookmarkOut])
def list_bookmarks(user_id: int = Query(..., ge=1)):
    _ensure_user(user_id)
    return _bookmarks.list_by_user(user_id)

@router.post("/", response_model=BookmarkOut)
def add_bookmark(payload: BookmarkIn, user_id: int = Query(..., ge=1)):
    _ensure_user(user_id)
    try:
        new_id = _bookmarks.add(user_id, payload.dict())
        return BookmarkOut(id=new_id, **payload.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{bookmark_id}")
def delete_bookmark(bookmark_id: int, user_id: int = Query(..., ge=1)):
    _ensure_user(user_id)
    _bookmarks.remove(user_id, bookmark_id)
    return {"message": "Bookmark removed"}
