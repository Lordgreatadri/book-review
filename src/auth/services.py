from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import desc, select
from src.auth.models import User
from src.auth.schemas import CreateUserModel
from src.auth.utils import hash_password, verify_password

class UserService(object):
    async def get_user_by_username(self, username: str, session: AsyncSession):
        statement = select(User).where(User.username == username)
        result = await session.execute(statement)
        user = result.scalars().first()

        return user if user is not None else False
    
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        user = result.scalars().first()

        return user if user is not None else False
    
    async def get_user_by_phone_number(self, phone_number: str, session: AsyncSession):
        statement = select(User).where(User.phone_number == phone_number)
        result = await session.execute(statement)
        user = result.scalars().first()

        return user if user is not None else False

    async def user_exists(self, username: str, email:str, session: AsyncSession):
        statement = select(User).where(User.username == username).where(User.email == email)
        result = await session.execute(statement)
        user = result.scalars().first()
        return True if user is not None else False

    async def create_user(self, user_data: CreateUserModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        user = User(**user_data_dict)
        user.password = hash_password(user_data_dict['password'])
        
        session.add(user)
        await session.commit()
        return user

    
    async def authenticate_user(self, username: str, password: str, session: AsyncSession):
        user = await self.get_user_by_username(username, session)
        if not user:
            return False
        
        if not verify_password(password, user.password):
            return False
        
        return user