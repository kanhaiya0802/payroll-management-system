from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user
from models import Employee

router = APIRouter(prefix="/employee", tags=["Employee Access"])


@router.get("/profile")
def my_profile(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user.role != "employee":
        raise HTTPException(status_code=403, detail="Employee access only")

    if not user.employee_id:
        raise HTTPException(status_code=400, detail="Employee account not linked with employee record")

    emp = db.query(Employee).filter(Employee.id == user.employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee record not found")

    return {
        "id": emp.id,
        "emp_code": emp.emp_code,
        "full_name": emp.full_name,
        "email": emp.email,
        "phone": emp.phone,
        "designation": emp.designation,
        "department": emp.department,
        "basic_salary": float(emp.basic_salary),
        "joining_date": str(emp.joining_date) if emp.joining_date else None
    }
