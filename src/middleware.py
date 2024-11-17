from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import FastAPI, status
from datetime import datetime
import time

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware


import logging
from src.config import Config


logger = logging.getLogger('uvicorn.access')
logger.disabled = True


# Initialize the limiter with a key function (e.g., based on IP address)
limiter = Limiter(key_func=get_remote_address)


def register_middleware(app: FastAPI):
    # Add your middleware here
    # @app.middleware('http')
    # async def app_access_control(request: Request, call_next):
    #     # Add your access control logic here
    #     # Example: Check if the client is authorized to access the API
    #     client_ip = request.client.host
    #     client_port = request.client.port
        
    #     if client_ip not in Config.allowed_hosts:
    #         logger.warning(f"Access denied from {client_ip}:{client_port}")
            
    #         return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"status_code":status.HTTP_403_FORBIDDEN ,"message": "Access denied"})
        
    #     response = await call_next(request)
    #     return response





     # Custom rate limit exception handler
    # @app.exception_handler(RateLimitExceeded)
    # async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    #     return JSONResponse(
    #         status_code=status.HTTP_429_TOO_MANY_REQUESTS,
    #         content={
    #             "status_code": status.HTTP_429_TOO_MANY_REQUESTS,
    #             "message": "Too many requests",
    #             "detail": "Rate limit exceeded. Please try again later."
    #             }
    #     )
 


    @app.middleware('http')
    async def app_custom_logger(request: Request, call_next):
        start_time = time.time()
        today = datetime.now()

        response = await call_next(request)
        processing_time = time.time() - start_time

        message = f"[{today}] - {request.client.host}:{request.client.port} - {request.method} - {request.url.path} ||  {response.status_code} - processed in {processing_time:.2f} seconds"
        logger.info(message)

        # Log the request details
        print(message)

        return response
    




    @app.middleware('http')
    async def authorization(request: Request, call_next):
        if not "Authorization" in request.headers:
            logger.warning(f"Authorization header not found in request from {request.client.host}:{request.client.port}")


            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status_code": status.HTTP_401_UNAUTHORIZED, "message": "Authorization header not set", "resolution":"Provide credentials to proceed."})
        
        authorization_header = request.headers.get("Authorization")
        if not authorization_header.startswith("Bearer "):
            logger.warning(f"Invalid authorization header in request from {request.client.host}:{request.client.port}")
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status_code": status.HTTP_401_UNAUTHORIZED, "message": "Invalid authorization header", "resolution":"Bearer token is required"})
        

        response = await call_next(request)
        return response


 
    app.add_middleware(
        CORSMiddleware, 
        allow_origins= ["*"],
        allow_methods = ["*"],
        allow_headers = ["*"],
        allow_credentials =True
                       
    )


    # app.add_middleware(
    #     TrustedHostMiddleware,
    #     allowed_hosts=Config.allowed_hosts
    # )



    # Add SlowAPI middleware for rate limiting
    # app.state.limiter = limiter
    # app.add_middleware(SlowAPIMiddleware)