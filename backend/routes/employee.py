from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database import get_db
from models import Employee
from schemas import EmployeeCreate, EmployeeOut
from dependencies import admin_only

from models import User
from auth import hash_password
from schemas import EmployeeLoginCreate


router = APIRouter(prefix="/employees", tags=["Employees"])

@router.post("/", response_model=EmployeeOut)
def add_employee(
    emp: EmployeeCreate,
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    existing = db.query(Employee).filter(
        or_(Employee.emp_code == emp.emp_code, Employee.email == emp.email)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Employee already exists")

    new_emp = Employee(**emp.model_dump())
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return new_emp


@router.get("/", response_model=list[EmployeeOut])
def list_employees(
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    return db.query(Employee).all()

@router.post("/{employee_id}/create-login")
def create_employee_login(
    employee_id: int,
    data: EmployeeLoginCreate,
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    # 1) Check employee exists
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    # 2) Email must match employee email 
    if emp.email != data.email:
        raise HTTPException(status_code=400, detail="Email must match employee email")

    # 3) Check user already exists
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Login already exists for this employee")

    # 4) Create user login
    user = User(
        full_name=emp.full_name,
        email=data.email,
        password_hash=hash_password(data.password),
        role="employee",
        employee_id=emp.id,
        must_change_password=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "Employee login created ✅", "employee_id": employee_id, "user_id": user.id}

@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Optional: delete linked login also
    user = db.query(User).filter(User.employee_id == employee_id).first()
    if user:
        db.delete(user)

    db.delete(emp)
    db.commit()

    return {"message": "Employee deleted ✅"}
