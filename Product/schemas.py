# To share product data with end users, create a structured Pydantic data model first

from pydantic import BaseModel

class Product(BaseModel):
    name: str
    description: str
    price: int

class DisplayProduct(BaseModel):
    name: str
    description: str

    class Config:
        from_attributes = True
        
class Seller(BaseModel):
    username: str
    email: str
    password: str

class DisplaySeller(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True

