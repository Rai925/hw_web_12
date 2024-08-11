from typing import Optional
from pydantic import BaseModel, EmailStr

class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: Optional[str] = None
    additional_info: Optional[str] = None

class ContactUpdate(ContactCreate):
    pass

class ContactResponse(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    birthday: Optional[str] = None
    additional_info: Optional[str] = None

    class Config:
        from_attributes = True
