from fastapi import FastAPI, HTTPException, status
from sqlalchemy.sql.functions import mode
from fastapi.params import Depends
from sqlalchemy.orm import Session
from . import schemas
from . import models
from .database import engine, Base, SessionLocal
from .models import Product
from typing import List
from passlib.context import CryptContext

app = FastAPI(
    title="Products API written by Patrick Yip",
    description="Get details for all the products on my website",
    terms_of_service="https://www.wisecrackr.com/terms",
    contact={
        "Developer name": "Patrick Yip",
        "website": "https://www.wisecrackr.com",
        "email": "support@wisecrackr.com"
    },
    # docs_url = "/documentation",
    # redoc_url = None
)

Base.metadata.create_all(engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.delete('/product/{id}', tags=['Products'])
def delete(id: int, db: Session = Depends(get_db)):
    result = db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    if result == 0:
        raise HTTPException(status_code=404, detail=f"Product with id {id} not found")
    db.commit()
    return {'message': 'Product deleted successfully', 'id': id}


@app.put('/product/{id}', tags=['Products'])
def update(id: int, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        pass
    product.update(request.model_dump())
    db.commit()
    return {f'Product: {id} is successfully updated'}


# @app.get('/products')
@app.get('/products', response_model = List[schemas.DisplayProduct], tags=['Products'])
def products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@app.get('/product/{id}', response_model = schemas.DisplayProduct, tags=['Products'])
def product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {id} not found")
    return product

@app.post('/product', status_code=status.HTTP_201_CREATED, tags=['Products'])
def add(request: schemas.Product, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=request.name, 
        description=request.description, 
        price=request.price,
        seller_id = 1
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# @app.post('/seller', response_model = schemas.DisplaySeller)
@app.post('/seller', tags=['Seller'])
def create_seller(request: schemas.Seller, db: Session = Depends(get_db)):
    hashedpassword = pwd_context.hash(request.password)
    new_seller = models.Seller(
        username = request.username, 
        email = request.email, 
        password = hashedpassword
    )
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller

