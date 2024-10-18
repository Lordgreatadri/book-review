from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .utils import verify_access_token


class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)
        


    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        token = await super().__call__(request)
        
        if not self.is_valid_token(token.credentials):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token not valid")
        
        # Verify token 
        token_data = verify_access_token(token.credentials)
        if token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide valid access_token")

        # print(token.credentials)

        return token_data

    
    def is_valid_token(self, token: str)-> bool:
        token_data = verify_access_token(token)

        return True if token_data is not None else False
