from passlib.context import CryptContext
from datetime import datetime, timedelta
from src.config import Config
import jwt # Make sure this is the PyJWT package
import uuid
import logging

#define password encryption algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#pip install python-jose[cryptography]     => old way but still works#-

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, db_password: str)-> bool:
    return pwd_context.verify(plain_password, db_password)


def create_access_token(user_data:dict, expiry:timedelta = None, refresh: bool = False)-> dict:

    to_encode = user_data.copy()

    expire_minutes = expiry if expiry is not None else timedelta(minutes=Config.access_token_expire_minutes)
    expire_time = datetime.utcnow() + expire_minutes

    to_encode.update(
        {
            "jti":str(uuid.uuid4()), 
            "exp": expire_time.timestamp(),  # UNIX timestamp
            "refresh":refresh
        }
    )

    token = jwt.encode(
        to_encode,
        Config.jwt_secret_key,
        Config.jwt_algorithm
    )

    return {"access_token": token}



def verify_access_token(token: str)-> dict:
    try:
        return jwt.decode(token, Config.jwt_secret_key, algorithms=[Config.jwt_algorithm])

    except jwt.ExpiredSignatureError as exp:
        logging.error(f"Access token expired at {exp}")

        # return {"error": "Token expired"}
        return None
    except jwt.InvalidTokenError as invalidErr:
        logging.error(f"Invalid access token: {invalidErr}")
        # return {"error": "Invalid token"}
        return None
    except jwt.InvalidKeyError as invalidKeyErr:
        logging.error(f"Invalid secret key: {invalidKeyErr}")
        # return {"error": "Invalid secret key"}
        return None
    except jwt.JWTError as jwtError:
        logging.error(f"An error occurred while decoding access token: {jwtError}")
        # return {"error": "An error occurred while decoding access token"}
        return None
    except Exception as e:
        logging.error(f"An error occurred while verifying access token: {e}")
        # return {"error": "An error occurred while verifying access token"}
        return None