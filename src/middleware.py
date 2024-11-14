from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import FastAPI, status
from datetime import datetime
import time




import logging
from src.config import Config


logger = logging.getLogger('uvicorn.access')
logger.disabled = True

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




    @app.middleware('http')
    async def rate_limit(request:Request, call_next):
        # Add your rate limiting logic here
        # Example: Implement a simple rate limiter
        client_ip = request.client.host
        client_port = request.client.port

        # # Check if the client has exceeded the rate limit
        # if client_ip in Config.rate_limit_cache:
        #     client_requests = Config.rate_limit_cache[client_ip]
        #     if client_requests >= Config.rate_limit_per_minute:
        #         logger.warning(f"Rate limit exceeded for {client_ip}:{client_port}")
                
        #         return JSONResponse(status_code=status.HTTP_429_TOO_MANY_REQUESTS, content={"status_code": status.HTTP_429_TOO_MANY_REQUESTS, "message": "Rate limit exceeded", "resolution":"Please try again later."})
            

        # # Increment the client's request count
        # if client_ip not in Config.rate_limit_cache:
        #     Config.rate_limit_cache[client_ip] = 1
        # else:
        #     Config.rate_limit_cache[client_ip] += 1


        return await call_next(request)


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
        
        bearer_token = authorization_header.split(" ")[1]
        
        # Validate the bearer token with your authorization logic
        # Example: Check if the bearer token is valid and has access to the API

        # If the token is valid, continue with the request
        # If the token is invalid, return a 401 Unauthorized response
        # If the token is revoked, return a 401 Unauthorized response
        
        # If the token is valid, continue with the request
        response = await call_next(request)
        return response


 
    app.add_middleware(
        CORSMiddleware, 
        allow_origins= ["*"],
        allow_methods = ["*"],
        allow_headers = ["*"],
        allow_credentials =True
                       
    )


    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=Config.allowed_hosts
    )
