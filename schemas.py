from pydantic import BaseModel

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
