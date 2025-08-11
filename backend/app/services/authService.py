from typing import Optional
from fastapi import HTTPException
from repositories.userRepo import UserRepository

class AuthService:
    def __init__(self, repo: Optional[UserRepository] = None) -> None:
        self.repo = repo or UserRepository()

    def register(self, username: str, password: str) -> dict:
        try:
            user_id = self.repo.create_user(username, password)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return {"id": user_id, "username": username}

    def login(self, username: str, password: str) -> dict:
        user = self.repo.get_user_by_credentials(username, password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user

