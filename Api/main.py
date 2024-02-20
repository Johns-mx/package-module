import uvicorn, pytz
from typing import Annotated
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from Api.Config.methods import version
from Api.Routers import package, user
from Api.Schemas.schemas import User, UserInDB, Token, TokenData


app = FastAPI(
    title="Package Module Api",
    version=version.ver
)


origins= ["http://localhost:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(package.package_router, prefix=f"/api/v{version.major}/package")
app.include_router(user.user_router, prefix=f"/api/v{version.major}/user")


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)