# To share product data with end users, create a structured Pydantic data model first

from pydantic import BaseModel

class Product(BaseModel):
    name: str
    description: str
    price: int

