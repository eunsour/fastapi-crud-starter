from os import environ

from fastapi import FastAPI, Depends, Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from sqlalchemy import Column, TIMESTAMP, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import FetchedValue

app = FastAPI()

SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}:{}/{}'.format(
        environ.get("DB_USER"), 
        environ.get("DB_PASSWORD"),
        environ.get("DB_HOST"), 
        environ.get("DB_PORT"), 
        environ.get("DB_NAME")
    )

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def session():
    db = Session()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base(bind=engine)

# Entity Item
class Item(Base):
    __tablename__ = "item"
    __table_args__ = {"autoload": True}
    item_id = Column(Integer, primary_key = True, nullable=False)
    name = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, FetchedValue())
    updated_at = Column(TIMESTAMP, FetchedValue())

# Request Body
class ItemRequest(BaseModel):
    name: str = Query(..., max_length=50)
    price: float


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/item")
def get_item(id: int = None, name: str = Query(None, max_length=50), db: Session = Depends(session)):
    if id is not None:
        result_set = db.query(Item).filter(Item.item_id == id).all()
    elif name is not None:
        result_set = db.query(Item).filter(Item.name == name).all()
    else:
        result_set = db.query(Item).all()    
    response_body = jsonable_encoder({"list": result_set})
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)

@app.post("/item")
def create_item(request: ItemRequest, db: Session = Depends(session)):
    item = Item(
                name = request.name,
                price = request.price
            )
    db.add(item)
    db.commit()
    response_body = jsonable_encoder({"item_id" : item.item_id})
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)

@app.put("/item/{id}")
def update_item(id: int, request: ItemRequest, db: Session = Depends(session)):
    item = db.query(Item).filter(Item.item_id == id).first()
    if item is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)
    item.name = request.name
    item.price = request.price
    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK)

@app.delete("/item/{id}")
def delete_item(id: int, db: Session = Depends(session)):
    db.query(Item).filter(Item.item_id == id).delete()
    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK)
