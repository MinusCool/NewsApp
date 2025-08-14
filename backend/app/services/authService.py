import datetime, jwt
from passlib.hash import bcrypt
from fastapi import HTTPException, status
from repositories.userRepo import UserRepo
from core.config import settings

ALGO = "HS256"
class AuthService:
    def __init__(self):
        self.repo = UserRepo()
        self.secret = settings.JWT_SECRET

    def register(self, username: str, password: str) -> int:
        hashed = bcrypt.hash(password)
        try:
            return self.repo.create_user(username, hashed)
        except Exception:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    def login(self, username: str, password: str) -> str:
        user = self.repo.get_by_username(username)
        if not user or not bcrypt.verify(password, user["password"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        payload = {
            "sub": str(user["id"]),
            "username": user["username"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12),
        }
        token = jwt.encode(payload, self.secret, algorithm=ALGO)
        return token

    def decode(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.secret, algorithms=[ALGO])
        except jwt.PyJWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


