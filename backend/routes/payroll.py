from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies import admin_only, get_current_user
from models import Payroll, Employee, Attendance
from schemas import PayrollGenerateRequest, PayrollOut

router = APIRouter(prefix="/payroll", tags=["Payroll"])


@router.post("/generate", response_model=PayrollOut)
def generate_payroll(
    data: PayrollGenerateRequest,
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    # validations
    if not (1 <= data.month <= 12):
        raise HTTPException(status_code=400, detail="Month must be 1-12")

    emp = db.query(Employee).filter(Employee.id == data.employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    att = db.query(Attendance).filter(
        Attendance.employee_id == data.employee_id,
        Attendance.month == data.month,
        Attendance.year == data.year
    ).first()

    if not att:
        raise HTTPException(status_code=404, detail="Attendance not found for this month/year")

    # Calculate salary
    basic_salary = float(emp.basic_salary)

    hra = basic_salary * 0.20
    da = basic_salary * 0.10
    gross = basic_salary + hra + da
    pf = basic_salary * 0.12

    ratio = att.days_present / att.total_working_days
    net_salary = (gross - pf) * ratio

    # check if payroll already exists
    existing = db.query(Payroll).filter(
        Payroll.employee_id == data.employee_id,
        Payroll.month == data.month,
        Payroll.year == data.year
    ).first()

    if existing:
        existing.basic_salary = basic_salary
        existing.hra = hra
        existing.da = da
        existing.pf = pf
        existing.days_present = att.days_present
        existing.total_working_days = att.total_working_days
        existing.net_salary = net_salary
        db.commit()
        db.refresh(existing)
        return existing

    payroll = Payroll(
        employee_id=data.employee_id,
        month=data.month,
        year=data.year,
        basic_salary=basic_salary,
        hra=hra,
        da=da,
        pf=pf,
        days_present=att.days_present,
        total_working_days=att.total_working_days,
        net_salary=net_salary
    )

    db.add(payroll)
    db.commit()
    db.refresh(payroll)
    return payroll


@router.get("/{employee_id}", response_model=list[PayrollOut])
def payroll_history(
    employee_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    return db.query(Payroll).filter(Payroll.employee_id == employee_id).all()


#  Employee limited payslip
@router.get("/employee/me", response_model=list[PayrollOut])
def my_payslips(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.role != "employee":
        raise HTTPException(status_code=403, detail="Employee access only")

    if not user.employee_id:
        raise HTTPException(status_code=400, detail="Employee not linked")

    return db.query(Payroll).filter(Payroll.employee_id == user.employee_id).all()
