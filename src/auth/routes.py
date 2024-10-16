from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from fastapi.responses import JSONResponse
from .models import User
from .schemas import CreateUserModel, UserModel,UserLoginModel
from src.db.main import get_session
from .services import UserService
from .utils import create_access_token, verify_access_token
from datetime import timedelta
from src.config import Config

auth_router = APIRouter()
user_service = UserService()

@auth_router.post("/register", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUserModel, session = Depends(get_session)):
    if await user_service.user_exists(user.email, user.username, session=session):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")

    if await user_service.get_user_by_email(user.email, session):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email already registered")
    
    if await user_service.get_user_by_username(user.username, session):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Username already registered")
    
    if await user_service.get_user_by_phone_number(user.phone_number, session):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Phone number already registered")
    
    new_user = await user_service.create_user(user, session)

    if new_user:
        return new_user
    
    raise HTTPException(status_code=500, detail="An error occurred while creating the user")


@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def login(user: UserLoginModel, session: Session = Depends(get_session)):
    user = await user_service.authenticate_user(user.username, user.password, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    access_token = create_access_token({
        "email": user.email,
        "user_uuid": str(user.uid)
    })#,timedelta(minutes=30)


    refresh_token = create_access_token(user_data={
        "email": user.email,
        "user_uuid": str(user.uid)
    }, expiry=timedelta(days=Config.refresh_token_expire_minutes), refresh=True)


    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "user": {
                "email": user.email,
                "user_uuid": str(user.uid),
                "phone_number": user.phone_number,
                "name": user.first_name +" "+user.last_name,
                "is_verified":user.is_verified
            },
            "access_token": access_token['access_token'],
            "refresh_token": refresh_token['access_token'],
            "token_type": "bearer",
            "message": "Login successful"
        }
    )


