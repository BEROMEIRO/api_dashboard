from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, reset_database 

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à minha API! Vá para /docs para explorar."}

@app.get("/items", response_model=list[schemas.ItemResponse])
def read_items(db: Session = Depends(get_db)):
    return crud.get_items(db)

@app.post("/items", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)

@app.delete("/items/clean_empty")
def clean_empty_items(db: Session = Depends(get_db)):
    crud.delete_empty_items(db)
    return {"message": "Itens vazios removidos com sucesso"}

@app.patch("/items/{item_id}/reduce_stock")
def reduce_stock(item_id: int, quantity: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item:
        item.stock -= quantity
        db.commit()
        db.refresh(item)
        return item
    return {"error": "Item não encontrado"}


# @app.on_event("startup")
# def startup():
#     reset_database() 
