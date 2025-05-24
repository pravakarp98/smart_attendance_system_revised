from bson import ObjectId
from fastapi import FastAPI, HTTPException
from app.core.security import pwd_context
from app.db.connection import admins_collection, students_collection

def to_object_id(id_str: str):
    try:
        return ObjectId(id_str)
    except:
        raise HTTPException(status_code=400, detail="Invalid ObjectId")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def email_exists(email: str, user_type: str) -> bool:
    if user_type == "admin":
        return admins_collection.find_one({"email": email}) is not None
    elif user_type == "student":
        return students_collection.find_one({"email": email}) is not None
