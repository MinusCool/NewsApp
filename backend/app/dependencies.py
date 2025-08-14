from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from services.authService import AuthService

auth_scheme = HTTPBearer()
_auth = AuthService()

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> dict:
    data = _auth.decode(creds.credentials)
    return {"id": int(data["sub"]), "username": data["username"]}
