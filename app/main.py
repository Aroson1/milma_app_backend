from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
import uvicorn
from databse import get_db
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import models
from databse import engine
from schemas import Products, Users, CurrentOrders
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='postgres', user='postgres',
                                password='qwerty', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database succesfully connected')
        break
    except Exception as error:
        print('connection failed')
        print('error:', error)
        time.sleep(3)

app = FastAPI()

models.Base.metadata.create_all(bind= engine)

@app.get("/ping")
def posts():
    return {"message": "You are currently connected to the server"}


### CRUD OPERATIONS FOR ITEMS
@app.post("/product")
def create(product: Products,db: Session = Depends(get_db)):
    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/product")
def get(db: Session = Depends(get_db)):
    all_products = db.query(models.Product).all()
    return all_products

@app.delete("/delete/product/{id}")
def delete(id:int ,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT):
    delete_post = db.query(models.Product).filter(models.Product.id == id)
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"product with such id does not exist")
    else:
        delete_post.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/update/product/{id}")
def update(id: int, product:Products, db:Session = Depends(get_db)):
    updated_post = db.query(models.Product).filter(models.Product.id == id)
    updated_post.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with such id: {id} does not exist')
    else:
        updated_post.update(product.dict(), synchronize_session=False)
        db.commit()
    return updated_post.first()
###--------------------------------------------###

### CRUD OPERATIONS FOR USERS
@app.post("/user")
def create(user: Users, db: Session = Depends(get_db)):
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/user")
def get(db: Session = Depends(get_db)):
    all_users = db.query(models.Users).all()
    return all_users

@app.delete("/delete/user/{id}")
def delete(id:int ,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT):
    delete_user = db.query(models.Users).filter(models.Users.id == id)
    if delete_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with such id does not exist")
    else:
        delete_user.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/update/user/{id}")
def update(id: int, user:Users, db:Session = Depends(get_db)):
    updated_user = db.query(models.Users).filter(models.Users.id == id)
    updated_user.first()
    if updated_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with such id: {id} does not exist')
    else:
        updated_user.update(user.dict(), synchronize_session=False)
        db.commit()
    return updated_user.first()
###--------------------------------------------###

### CRUD OPERATIONS FOR CURRENT ORDERS
@app.post("/order")
def create(order: CurrentOrders, db: Session = Depends(get_db)):
    new_order = models.CurrentOrders(**order.dict())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@app.get("/order")
def get(db: Session = Depends(get_db)):
    all_orders = db.query(models.CurrentOrders).all()
    return all_orders

@app.delete("/delete/order/{id}")
def delete(id:int ,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT):
    delete_order = db.query(models.CurrentOrders).filter(models.CurrentOrders.id == id)
    if delete_order == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"order with such id does not exist")
    else:
        delete_order.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
###--------------------------------------------###



if __name__ == "__main__":
    uvicorn.run("main:app", port=3000, log_level="info", reload=True)