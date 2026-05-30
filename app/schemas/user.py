from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


class UserResponse(UserBase):
    id: UUID
    full_name: Optional[str] = None
    is_superuser: bool = False

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None
