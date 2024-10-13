from passlib.context import CryptContext
#define password encryption algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



#pip install python-jose[cryptography]     => old way but still works

def hash_password(password:str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, db_password: str)-> bool:
    return pwd_context.verify(plain_password, db_password)