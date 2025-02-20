# app/main.py
from fastapi import FastAPI, HTTPException, Depends
from auth import AuthMiddleware, create_access_token
from routes import items, health
from models import User, Item  # Import your models
from db import engine, get_db, Base  # Import Base
from sqlalchemy.orm import Session

# Create the tables if they don't exist (using create_all)
Base.metadata.create_all(bind=engine)  # This is the key line

app = FastAPI()

app.add_middleware(AuthMiddleware)

app.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(health.router, prefix="/health", tags=["health"])

@app.post("/token")
async def login(db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == "testuser").first()  # Replace with your logic
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)