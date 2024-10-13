from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from .models import User
from .schemas import CreateUserModel, UserModel,UserLoginModel
from src.db.main import get_session
from .services import UserService

auth_router = APIRouter()
user_service = UserService()

@auth_router.post("/register", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def login(user: CreateUserModel, session = Depends(get_session)):
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


@auth_router.post('/login', response_model=UserModel, status_code=status.HTTP_200_OK)
async def login_user(user: UserLoginModel, session: Session = Depends(get_session)):
    user = await user_service.authenticate_user(user.username, user.password, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    return user


