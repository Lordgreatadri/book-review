from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .utils import verify_access_token


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)
        


    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        token = await super().__call__(request)
        
        if not self.is_valid_token(token.credentials):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token not valid")
        
        # Verify token 
        token_data = verify_access_token(token.credentials)

        # print(token.credentials)
        self.verify_token_data(token_data)
        
        return token_data
 
    
    def is_valid_token(self, token: str)-> bool:
        token_data = verify_access_token(token)

        # return True if token_data is not None else False
        return token_data is not None


    def verify_token_data(self, token_data: dict):
        raise NotImplementedError("Please override this method in your child class.")
    



class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Please provide a valid access_token"
            )







class RefereshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Please provide a valid refresh_token"
            )