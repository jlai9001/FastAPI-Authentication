from pydantic import BaseModel
from enum import Enum


class UserCreate(BaseModel):
    email:str
    password:str

class UserResponse(BaseModel):
    id:int
    email:str
    password:bytes
    logged_in:bool

# OAuth - Token
class Token(BaseModel):
    access_token:str
    token_type:str

# Stripe Payment
class PurchaseRequest(BaseModel):
    name: str
    price: int

# File Types (Enum)
class FileType(str, Enum):
    pdf = "pdf"
    image = "image"
    text ="text"

class FileRequest(BaseModel):
    filename: str
    file_type: FileType
