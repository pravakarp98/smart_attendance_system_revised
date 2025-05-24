from backend.app.schemas.models import (
    AdminLogin, 
    AdminSignup, 
    StudentLogin, 
    StudentSignup, 
    StudentUpdate,
    FilterCriteria
)
from app.db.connection import admins_collection, students_collection
from fastapi import FastAPI, HTTPException, Depends, Body
from core.rate_limiter import rate_limiter
from core.security import create_jwt_token
from utils.helper import to_object_id

app = FastAPI()

# Admin Signup
@app.post(f"/v1/org/admin/signup")
async def admin_signup(admin: AdminSignup):
    if admins_collection.find_one({"username": admin.username}):
        raise HTTPException(status_code=400, detail="Admin username already exists")
    admins_collection.insert_onw(admin.dict())
    return {"message": "Admin registered successfully"}

# Admin Login
@app.post(f"/v1/org/admin/login")
async def admin_login(admin: AdminLogin):
    existing_admin = admins_collection.find_one({"username": admin.username})
    if not existing_admin or existing_admin.get("password") != admin.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_jwt_token({"username": admin.username, "role": "admin"})
    return {"access_token": token}

# Student Signup
@app.post(f"/v1/org/student/signup")
async def student_signup(student: StudentSignup):
    if students_collection.find_one({"email": student.email}):
        raise HTTPException(status_code=400, detail="Student email already exists")
    students_collection.insert_one(student.dict())
    return {"message": "Student registered successfully"}

# Student Login
@app.post(f"/v1/org/student/login")
async def student_login(student: StudentLogin):
    existing_student = students_collection.find_one({"email": student.email})
    if not existing_student or existing_student.get("password") != student.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_jwt_token({"email": student.email, "role": "student"})
    return {"access_token": token}

# CRUD Operations for Student Data
@app.get(f"/v1/org/student/{{student_id}}", dependencies=[Depends(rate_limiter)])
async def get_student(student_id: str):
    student = students_collection.find_one({"_id": to_object_id(student_id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student["_id"] = str(student["_id"])
    return student

@app.put(f"/v1/org/student/{{student_id}}")
async def update_student(student_id: str, update_data: StudentUpdate):
    result = students_collection.update_one(
        {"_id": to_object_id(student_id)}, {"$set": update_data.dict(exclude_unset=True)}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student updated successfully"}

@app.delete(f"/v1/org/student/{{student_id}}")
async def delete_student(student_id: str):
    result = students_collection.delete_one({"_id": to_object_id(student_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}

# CRUD Operations for Admin Data
@app.get(f"/v1/org/admin/{{admin_id}}")
async def get_admin(admin_id: str):
    admin = admins_collection.find_one({"_id": to_object_id(admin_id)})
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    admin["_id"] = str(admin["_id"])
    return admin

@app.put(f"/v1/org/admin/{{admin_id}}")
async def update_admin(admin_id: str, update_data: AdminSignup):
    result = admins_collection.update_one(
        {"_id": to_object_id(admin_id)}, {"$set": update_data.dict(exclude_unset=True)}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Admin not found")
    return {"message": "Admin updated successfully"}

@app.delete(f"/v1/org/admin/{{admin_id}}")
async def delete_admin(admin_id: str):
    result = admins_collection.delete_one({"_id": to_object_id(admin_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Admin not found")
    return {"message": "Admin deleted successfully"}

# Filter Students
@app.post(f"/v1/org/students/filter")
async def filter_students(criteria: FilterCriteria):
    query = {key: value for key, value in criteria.dict().items() if value is not None}
    students = students_collection.find(query)
    return [{"_id": str(student["_id"]), **student} for student in students]