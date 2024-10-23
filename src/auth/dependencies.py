from typing import List
from fastapi import HTTPException, Request, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import decode_access_token
from src.db.redis import token_in_blocklist
from src.db.main import get_session
from . services import UserService
from . models import User



user_service = UserService()

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)
        


    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        token = await super().__call__(request)

        # decode token 
        token_data = decode_access_token(token.credentials)
        
        if not self.is_valid_token(token.credentials):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail={
                    "status_code":status.HTTP_403_FORBIDDEN,
                    "error":"Token is invalid or expired",
                    "resolution":"Please create a new token"
                }
            )
        
        
        #check if token is in the blocklist
        if await token_in_blocklist(token_data['jti']):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail={
                    "status_code":status.HTTP_403_FORBIDDEN,
                    "error":"Token is either revoked or invalid",
                    "resolution":"Please create a new token"
                    }
                )


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
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail={
                    "status_code":status.HTTP_403_FORBIDDEN,
                    "error":"Please provide a valid access_token"
                    }
            )







class RefereshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail={
                    "status_code":status.HTTP_403_FORBIDDEN,
                    "error":"Please provide a valid refresh_token"
                    }
            )
        








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
        print(self.allowed_roles)
        if current_user.role in self.allowed_roles:
            return True 
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "status_code": status.HTTP_403_FORBIDDEN,
                "error":"Access denied",
                "message":"You are not permitted to perform this action."
            }
        )