from fastapi import HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
import jwt

from models import User
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from db import get_db

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Exclude authentication for OpenAPI routes
        if request.url.path.startswith(("/docs", "/redoc", "/openapi.json", "/token")):
            return await call_next(request)

        token = request.headers.get("Authorization")
        if not token or " " not in token:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Missing or invalid token"})

        try:
            scheme, token = token.split(" ")
            if scheme.lower() != "bearer":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token scheme")

            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")

            # Create a new database session
            db = next(get_db())  
            user = self.get_user(user_id, db)
            db.close()  # Close the session

            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")

            request.state.user = user
            response = await call_next(request)
            return response

        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Token expired"})
        except jwt.InvalidTokenError:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Invalid token"})
        except Exception as e:
            print(f"Token error: {e}")
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Authentication error"})

    def get_user(self, user_id: int, db: Session) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
