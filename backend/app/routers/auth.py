from fastapi import APIRouter, Depends
from models.schemas import RegisterIn, LoginIn, TokenOut, UserOut
from services.authService import AuthService
from dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])
_service = AuthService()

@router.post("/register", status_code=201)
def register(data: RegisterIn):
    uid = _service.register(data.username, data.password)
    return {"id": uid, "username": data.username}

@router.post("/login", response_model=TokenOut)
def login(data: LoginIn):
    token = _service.login(data.username, data.password)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def me(current=Depends(get_current_user)):
    return current
