from typing import List
from fastapi import HTTPException, Request, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import decode_access_token
from src.db.redis import token_in_blocklist
from src.exceptions.errors import (
    UserAccountNotVerified,
    InsufficientPermission,
    RefreshTokenRequired,
    AccessTokenRequired,
    InvalidToken,
    RevokedToken,
    RevokedToken,
) 
from src.db.main import get_session
from . services import UserService
from src.db.models import User



user_service = UserService()

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)
        


    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        token = await super().__call__(request)

        # decode token 
        token_data = decode_access_token(token.credentials)
        
        if not self.is_valid_token(token.credentials):
            raise InvalidToken()
        
        
        #check if token is in the blocklist
        if await token_in_blocklist(token_data['jti']):
            raise RevokedToken()


        # print(token.credentials)
        self.verify_token_data(token_data)
        
        return token_data
 
    
    def is_valid_token(self, token: str)-> bool:
        token_data = decode_access_token(token)

        # return True if token_data is not None else False
        return token_data is not None


    def verify_token_data(self, token_data: dict):
        raise NotImplementedError("Please override this method in your child class.")
    



class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise AccessTokenRequired()
            



class RefereshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise RefreshTokenRequired()
        



async def get_current_user(
        token_details: dict = Depends(AccessTokenBearer()), 
        session:AsyncSession = Depends(get_session)
    ):

    current_user = await user_service.get_user_by_email(token_details['email'], session)

    return current_user




class RoleChecker():
    def __init__(self, allowed_roles:List[str]) -> None:
        self.allowed_roles = allowed_roles



    def __call__(self, current_user:User =Depends(get_current_user)):
        if not current_user.is_verified:
            raise UserAccountNotVerified()
        
        if current_user.role in self.allowed_roles:
            return True 
        
        raise InsufficientPermission()