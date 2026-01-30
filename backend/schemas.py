from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# -------- AUTH --------
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: str  # admin/employee

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


# -------- EMPLOYEE --------
class EmployeeCreate(BaseModel):
    emp_code: str
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    designation: Optional[str] = None
    department: Optional[str] = None
    basic_salary: float
    joining_date: Optional[date] = None

class EmployeeOut(BaseModel):
    id: int
    emp_code: str
    full_name: str
    email: EmailStr
    phone: Optional[str]
    designation: Optional[str]
    department: Optional[str]
    basic_salary: float

    class Config:
        from_attributes = True

class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: str  # "admin" or "employee"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class EmployeeLoginCreate(BaseModel):
    email: EmailStr
    password: str

class AttendanceUpsert(BaseModel):
    employee_id: int
    month: int   # 1 to 12
    year: int
    days_present: int
    total_working_days: int


class AttendanceOut(BaseModel):
    id: int
    employee_id: int
    month: int
    year: int
    days_present: int
    total_working_days: int

    class Config:
        from_attributes = True

class PayrollGenerateRequest(BaseModel):
    employee_id: int
    month: int
    year: int


class PayrollOut(BaseModel):
    id: int
    employee_id: int
    month: int
    year: int
    basic_salary: float
    days_present: int
    total_working_days: int
    net_salary: float
    hra: float
    da: float
    pf: float

    class Config:
        from_attributes = True

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
