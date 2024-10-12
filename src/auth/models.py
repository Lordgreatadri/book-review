from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date
from pydantic import BaseModel
import uuid


class User(SQLModel, table=True):
    __tablename__ = "users"
    uid:uuid.UUID= Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            nullable=False,
            default= uuid.uuid4,
            unique=True,
            index=True
        )
    )
    username:str
    email:str = Field(sa_column=Column(unique=True, nullable=False, index=True))
    phone_number:str = Field(sa_column=Column(unique=True, nullable=False,index=True))
    first_name:str
    last_name:str
    is_verified:bool=False
    created_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))


    def __repr__(self):
        return f"<User {self.username}>"
     
