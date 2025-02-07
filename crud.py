from sqlalchemy.orm import Session
import models, schemas

def get_items(db: Session):
    return db.query(models.Item).all()

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(
        name=item.name,
        description=item.description,
        price=item.price,  # Novo campo de preço
        category=item.category
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_empty_items(db: Session):
    db.query(models.Item).filter(
        (models.Item.name == "") | (models.Item.description == "")
    ).delete(synchronize_session=False)
    db.commit()
