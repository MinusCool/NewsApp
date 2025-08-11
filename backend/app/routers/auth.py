from fastapi import APIRouter
from models.schemas import RegisterRequest, LoginRequest, UserOut
from services.authService import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
_service = AuthService()

@router.post("/register", response_model=UserOut)
def register(payload: RegisterRequest):
    user = _service.register(payload.username, payload.password)
    return user

@router.post("/login", response_model=UserOut)
def login(payload: LoginRequest):
    user = _service.login(payload.username, payload.password)
    return user
