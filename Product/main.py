from fastapi import FastAPI, HTTPException
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
def delete(id: int, db: Session = Depends(get_db)):
    result = db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    if result == 0:
        raise HTTPException(status_code=404, detail=f"Product with id {id} not found")
    db.commit()
    return {'message': 'Product deleted successfully', 'id': id}


@app.put('/product/{id}')
def update(id: int, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        pass
    product.update(request.model_dump())
    db.commit()
    return {f'Product: {id} is successfully updated'}



@app.get('/products')
def products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@app.get('/product/{id}')
def product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {id} not found")
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

    