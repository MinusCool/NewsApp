from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models.schemas import BookmarkIn, BookmarkOut
from dependencies import get_current_user
from repositories.bookmarkRepo import BookmarkRepo

router = APIRouter(prefix="/bookmarks", tags=["bookmarks"])
repo = BookmarkRepo()

@router.get("", response_model=List[BookmarkOut])
def list_bookmarks(current=Depends(get_current_user)):
    rows = repo.list(current["id"])
    return rows

@router.post("", status_code=201)
def add_bookmark(data: BookmarkIn, current=Depends(get_current_user)):
    bid = repo.add(current["id"], data.model_dump())
    if bid == 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Bookmark already exists")
    return {"id": bid}

@router.delete("/{bookmark_id}", status_code=204)
def delete_bookmark(bookmark_id: int, current=Depends(get_current_user)):
    n = repo.delete(current["id"], bookmark_id)
    if n == 0:
        raise HTTPException(status_code=404, detail="Not found")
    return
