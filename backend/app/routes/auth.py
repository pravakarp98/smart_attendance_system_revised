from fastapi import APIRouter, HTTPException, Depends
from app.schemas.admin import AdminLogin
from app.core.security import create_jwt_token
from app.db.connection import admins_collection

router = APIRouter()

async def login_admin(admin: AdminLogin):
    user = admins_collection.find_one({"username": admin.username})
    if user and user["passworrd"] == admin.password:
        token = create_jwt_token({"username": admin.username, "role": "admin"})
        return {"access_token": token}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")