import smtplib
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi.responses import JSONResponse
from .schemas import CreateUserModel, EmailModel, UserModel,UserLoginModel, UserBooksModel
from src.db.main import get_session
from .services import UserService
from .utils import create_access_token, create_url_safe_token, decode_url_safe_token
from datetime import timedelta, datetime
from src.config import Config
from .dependencies import RefereshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from src.db.redis import add_jti_to_blocklist
from src.exceptions.errors import (
    UserPhoneNumberAlreadyExists,
    UserEmailAlreadyVerified,
    UserEmailAlreadyExists,
    InvalidUserCredentials,
    NewResourceServerError,
    InvalidVerificationUrl,
    UsernameAlreadyExists,
    UserAlreadyExists,
    InvalidToken,
    UserNotFound
) 

from src.mails.mail import mail, create_message


auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(Config.roles)

@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUserModel, session:AsyncSession = Depends(get_session)):
    if await user_service.user_exists(user.email, user.username, session=session):
        raise UserAlreadyExists()
    

    if await user_service.get_user_by_email(user.email, session):
        raise UserEmailAlreadyExists()
    

    if await user_service.get_user_by_username(user.username, session):
        raise UsernameAlreadyExists()
    
    
    
    if await user_service.get_user_by_phone_number(user.phone_number, session):
        raise UserPhoneNumberAlreadyExists()
    

    new_user = await user_service.create_user(user, session)

    if new_user:
        token = create_url_safe_token({"uuid": new_user.uid, "email": new_user.email, "username": new_user.username})
        # verify_url = f"http://{Config.domain_name}/api/v1/auth/verify/{token}"
        # email_message = f"""
        #     <h1>Verify Your eEmail</h1>
        #     <p>Please click <a href="{verify_url}">HERE</a> to verify your email</p>
        # """
        
        # message = create_message(
        #     recipients=[user.email],
        #     subject="Verify Your Email",
        #     body=email_message,
        # )
        # await mail.send_message(message)
        # print(token)
        return JSONResponse(
            status_code= status.HTTP_201_CREATED,
            content={
                "status_code": status.HTTP_201_CREATED,
                "user": {
                    "email": user.email,
                    "user_uuid": str(user.uid),
                    "phone_number": user.phone_number,
                    "name": user.first_name +" "+user.last_name,
                    "role": user.role,
                    "is_verified":user.is_verified
                },
                "message": "Account created successfully, please check email to verify your account."
            }
        )
    
    raise NewResourceServerError()



 
@auth_router.get("/verify/{token}", status_code=status.HTTP_200_OK)
async def verify_email(token: str, session: AsyncSession = Depends(get_session)) :
    token_data = decode_url_safe_token(token)
    
    if not token_data:
        raise InvalidVerificationUrl()

    email = token_data.get("email")

    if not email:
        raise InvalidVerificationUrl()
    
    user = await user_service.get_user_by_email(email, session)
    
    if not user:
        raise UserNotFound()
    
    if user.is_verified :
        raise UserEmailAlreadyVerified()
    
    user_data = {
        "is_verified": True
    }
    await user_service.update_user(email, user_data, session)

    access_token = create_access_token({
        "email": user.email,
        "user_uuid": str(user.uid),
        "role": user.role,
    })#,timedelta(minutes=30)


    refresh_token = create_access_token(user_data={
        "email": user.email,
        "user_uuid": str(user.uid)
    }, expiry=timedelta(days=Config.refresh_token_expire_minutes), refresh=True)
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status_code": status.HTTP_200_OK,
            "user": {
                "email": user.email,
                "user_uuid": str(user.uid),
                "phone_number": user.phone_number,
                "name": user.first_name +" "+user.last_name,
                "role": user.role,
                "is_verified":user.is_verified
            },
            "access_token": access_token['access_token'],
            "refresh_token": refresh_token['access_token'],
            "message": "Email verified successfully"
        }
    )





@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def login(user: UserLoginModel, session: AsyncSession = Depends(get_session)):
    user = await user_service.authenticate_user(user.username, user.password, session)
    if not user:
        raise InvalidUserCredentials()
    
    
    access_token = create_access_token({
        "email": user.email,
        "user_uuid": str(user.uid),
        "role": user.role,
    })#,timedelta(minutes=30)


    refresh_token = create_access_token(user_data={
        "email": user.email,
        "user_uuid": str(user.uid)
    }, expiry=timedelta(days=Config.refresh_token_expire_minutes), refresh=True)


    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status_code": status.HTTP_200_OK,
            "user": {
                "email": user.email,
                "user_uuid": str(user.uid),
                "phone_number": user.phone_number,
                "name": user.first_name +" "+user.last_name,
                "role": user.role,
                "is_verified":user.is_verified
            },
            "access_token": access_token['access_token'],
            "refresh_token": refresh_token['access_token'],
            "token_type": "bearer",
            "message": "Login successful"
        }
    )



@auth_router.get('/create_access_token', status_code=status.HTTP_200_OK)
async def generate_access_token(token_details:dict = Depends(RefereshTokenBearer())):
    expiry_time = token_details['exp']

    if datetime.fromtimestamp(expiry_time) > datetime.now():
        new_access_token = create_access_token({
            "email": token_details['email'],
            "user_uuid": token_details['user_uuid']
        })

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status_code": status.HTTP_200_OK,
                "access_token": new_access_token['access_token'],
                "token_type": "bearer",
                "message": "Access token refreshed successfully"
            }
        )
    
    raise InvalidToken()



@auth_router.get("/user", response_model=UserBooksModel)
async def get_user(user:dict = Depends(get_current_user), _:bool = Depends(role_checker)):
    return user



@auth_router.get('/logout')
async def revoke_token(token_detail:dict =Depends(AccessTokenBearer())):
    jti = token_detail['jti']
    await add_jti_to_blocklist(jti)
    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content={
            "status_code": status.HTTP_200_OK, 
            "message": "Logged out successfully"
            }
        )


@auth_router.post('/send-mail')
async def send_mail(email:EmailModel):

    try:
        server = smtplib.SMTP(Config.mail_host, Config.mail_port)
        server.starttls()
        server.login(Config.mail_username, Config.mail_password)

        print("Connection successful!")

        server.quit()

        emails = email.email_addresses

        html = "<h1>Welcome to the app</h1>"
        subject = "Welcome to our site!"

        message = create_message(
            recipients= emails,
            subject= subject,
            body= html
        )

        await mail.send_message(message)

        return {"message": "Email sent successfully"} 

    except Exception as e:
        print("Failed to connect:", e)

        return e

    

