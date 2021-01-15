from typing import List, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class User(UserBase):
    id: int
    service_id: int

    class Config:
        orm_mode = True


class ServiceBase(BaseModel):
    owner: str
    service: bytes


class Service(ServiceBase):
    id: int
    allowed: List[User]

    class Config:
        orm_mode = True

