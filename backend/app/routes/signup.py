from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from app.utils.helper import email_exists, hash_password
# from app.core.rate_limiter import rate_limiter
from app.schemas.models import AdminSignup
from app.db.connection import students_collection, admins_collection

router = APIRouter(prefix="/v1/signup", tags=["signup"])

@router.post("/admin_signup")
async def signup(request_body: AdminSignup):
    if email_exists(request_body.email, request_body.role):
        raise HTTPException(status_code=400, detail="Email already exists")

    # Hash the password before storing
    hashed_password = hash_password(request_body.password)
    user_data = {
        "name": request_body.name,
        "email": request_body.email,
        "password": hashed_password,
        "role": request_body.role,
    }

    # Insert the user data into the MongoDB collection
    result = admins_collection.insert_one(user_data)
    return {"message": "User registered successfully", "user_id": str(result.inserted_id)}