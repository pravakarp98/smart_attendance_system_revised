from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from app.utils.helper import email_exists, hash_password
# from app.core.rate_limiter import rate_limiter
from app.schemas.models import AdminSignup, StudentSignup
from app.db.connection import students_collection, admins_collection

router = APIRouter(prefix="/v1/signup", tags=["signup"])

@router.post("/admin_signup")
async def admin_signup(request_body: AdminSignup):
    if email_exists(request_body.email, request_body.role):
        raise HTTPException(status_code=400, detail="Email already registered")

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
    response = {"success": True, "message": "User registered successfully", "user_id": str(result.inserted_id)}

    return JSONResponse(content=response, status_code=200)

@router.post("/student_signup")
async def student_signup(request_body: StudentSignup):
    if email_exists(request_body.email, "student"):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(request_body.password)
    
    new_student = {
        "name": request_body.name,
        "email": request_body.email,
        "password": hashed_password,
        "department": request_body.department,
        "age": request_body.age,
    }
    
    result = students_collection.insert_one(new_student)
    response = {"success": True, "message": "Student registered successfully", "student_id": str(result.inserted_id)}
    
    return JSONResponse(content=response, status_code=200)