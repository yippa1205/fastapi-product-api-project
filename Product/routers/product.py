from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas
from .. import models
from typing import List

router = APIRouter()

@router.delete('/product/{id}', tags=['Products'])
def delete(id: int, db: Session = Depends(get_db)):
    result = db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    if result == 0:
        raise HTTPException(status_code=404, detail=f"Product with id {id} not found")
    db.commit()
    return {'message': 'Product deleted successfully', 'id': id}

@router.put('/product/{id}', tags=['Products'])
def update(id: int, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        pass
    product.update(request.model_dump())
    db.commit()
    return {f'Product: {id} is successfully updated'}


# @app.get('/products')
@router.get('/products', response_model = List[schemas.DisplayProduct], tags=['Products'])
def products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@router.get('/product/{id}', response_model = schemas.DisplayProduct, tags=['Products'])
def product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {id} not found")
    return product

@router.post('/product', status_code=status.HTTP_201_CREATED, tags=['Products'])
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