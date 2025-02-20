# app/models.py (Update your models to inherit from Base)
from typing import Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db import Base  # Import your Base

class Item(Base):  # Inherit from Base
    __tablename__ = "items" # Table name

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    # ... other user fields (e.g., hashed password)