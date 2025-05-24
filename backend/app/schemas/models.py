from pydantic import BaseModel, EmailStr
from typing import List, Optional
    
class AdminSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    
class AdminLogin(BaseModel):
    email: str
    password: str
    
class StudentSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    department: str
    age: int
    
class StudentLogin(BaseModel):
    email: EmailStr
    password: str
    
class StudentUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    departemnt: Optional[str]
    age: Optional[int]
    
class FilterCriteria(BaseModel):
    deparrtment: Optional[str]
    age: Optional[int]
    attendance_per_week: Optional[int]
    attendance_monthly: Optional[int]
    attendance_annually: Optional[int]
    