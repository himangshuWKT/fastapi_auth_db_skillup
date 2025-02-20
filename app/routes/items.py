from fastapi import APIRouter, Depends, Request, status
from typing import List
from sqlalchemy.orm import Session
from models import Item, User  # SQLAlchemy models
from schemas import ItemSchema  # Pydantic schema
from auth import AuthMiddleware
from db import get_db

router = APIRouter()

@router.get("", response_model=List[ItemSchema])  # Use Pydantic schema here
async def read_items(request: Request, db: Session = Depends(get_db)):
    user: User = request.state.user
    items = db.query(Item).all()  # Fetch SQLAlchemy items
    return items  # FastAPI will convert these to Pydantic schemas

@router.post("", response_model=ItemSchema, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemSchema, request: Request, db: Session = Depends(get_db)):
    user: User = request.state.user
    db_item = Item(**item.model_dump())  # Convert Pydantic model to SQLAlchemy model
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
