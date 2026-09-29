from pydantic import BaseModel , Field 

class Address(BaseModel):
    city: str = None
    street: str = None
    building: int = None



  
class reg_user(BaseModel):
    name : str = Field(min_length=5 , max_length=20)
    age : int = Field(ge=16 , le=80)
    email : str = Field(min_length=5 , max_length=20)
    password : str =Field(min_length=8 , max_length=20)
    address: Address


class login_user(BaseModel):
    email : str = Field(min_length=5 , max_length=20)
    password : str =Field(min_length=8 , max_length=20)