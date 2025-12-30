from fastapi import FastAPI
from sqlalchemy.sql.functions import mode
from fastapi.params import Depends
from sqlalchemy.orm import Session
from . import schemas
from . import models
from .database import engine, Base, SessionLocal
from .models import Product

app = FastAPI()

Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.delete('/product/{id}')
def delete(id, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {'product deleted'}

@app.get('/products')
def products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@app.get('/product/{id}')
def product(id, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    return product

@app.post('/product')
def add(request: schemas.Product, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=request.name, 
        description=request.description, 
        price=request.price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request

    