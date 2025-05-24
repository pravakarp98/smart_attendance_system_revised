from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
# from app.core.rate_limiter import rate_limiter
from app.schemas.models import AdminLogin, StudentLogin
from app.db.connection import students_collection, admins_collection
from app.core.security import create_jwt_token, verify_password

router = APIRouter(prefix="/v1/login", tags=["login"])

@router.post("/admin_login")
async def admin_login(request_body: AdminLogin):
    email, password = request_body.username.email, request_body.password
    
    try:
        user = admins_collection.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="Invalid credentials")
        
        if not verify_password(password, user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        token = create_jwt_token({"email": email})
        
        return JSONResponse(
            content={"success": True, "message": "Login successful", "access_token": token},
            status_code=200,
        )
        
    except HTTPException as e:
        raise e
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.post("/student-login")
async def login(request_body: StudentLogin):
    username, password = request_body.email, request_body.password
    
    try:
        user = students_collection.find_one({"email": username})
        if not user:
            raise HTTPException(status_code=404, detail="Invalid credentials")
        
        if not verify_password(password, user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        token = create_jwt_token({"email": username})
        
        return JSONResponse(
            content={"success": True, "message": "Login successful", "access_token": token},
            status_code=200
        )
        
    except HTTPException as e:
        raise e
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")