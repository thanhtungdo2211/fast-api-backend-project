from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models import Item
from database import get_db
from api.items.schema import Item, ItemCreate

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

@router.get("/", response_model=List[Item])
def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all items"""
    items = db.query(Item).offset(skip).limit(limit).all()
    return items

@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Get a specific item by ID"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/", response_model=Item)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    # Check if the item with the same name already exists
    existing_item = db.query(Item).filter(Item.name == item.name).first()
    if existing_item:
        raise HTTPException(status_code=400, detail="Item already exists.")
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item