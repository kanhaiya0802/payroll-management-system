from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies import admin_only
from models import Attendance, Employee
from schemas import AttendanceUpsert, AttendanceOut

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/", response_model=AttendanceOut)
def upsert_attendance(
    data: AttendanceUpsert,
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    # check employee exists
    emp = db.query(Employee).filter(Employee.id == data.employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    # validations
    if not (1 <= data.month <= 12):
        raise HTTPException(status_code=400, detail="Month must be 1-12")
    if data.total_working_days <= 0:
        raise HTTPException(status_code=400, detail="Total working days must be > 0")
    if data.days_present < 0 or data.days_present > data.total_working_days:
        raise HTTPException(status_code=400, detail="Invalid days_present value")

    record = db.query(Attendance).filter(
        Attendance.employee_id == data.employee_id,
        Attendance.month == data.month,
        Attendance.year == data.year
    ).first()

    if record:
        record.days_present = data.days_present
        record.total_working_days = data.total_working_days
        db.commit()
        db.refresh(record)
        return record

    new_record = Attendance(
        employee_id=data.employee_id,
        month=data.month,
        year=data.year,
        days_present=data.days_present,
        total_working_days=data.total_working_days
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


@router.get("/{employee_id}", response_model=list[AttendanceOut])
def list_attendance(
    employee_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    return db.query(Attendance).filter(Attendance.employee_id == employee_id).all()
