import os
import calendar
from reportlab.lib.utils import ImageReader
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import BytesIO
from datetime import datetime

from database import get_db
from dependencies import get_current_user
from models import Payroll, Employee

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

router = APIRouter(prefix="/payslip", tags=["Payslip PDF"])


@router.get("/download/{payroll_id}")
def download_payslip_pdf(
    payroll_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # get payroll record
    payroll = db.query(Payroll).filter(Payroll.id == payroll_id).first()
    if not payroll:
        raise HTTPException(status_code=404, detail="Payroll record not found")

    # employee record
    emp = db.query(Employee).filter(Employee.id == payroll.employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    #  employee can download only own payslip
    if user.role == "employee":
        if not user.employee_id or user.employee_id != emp.id:
            raise HTTPException(status_code=403, detail="Not allowed")

    #  create PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    #page border
    c.rect(40, 40, width - 80, height - 80)


    y = height - 140

    downloaded_date = datetime.now().strftime("%d-%m-%Y %I:%M %p")

    # Header
    # Company header
    company_name = "ABC Tech Pvt. Ltd."
    company_tagline = "Payroll Department"

    logo_path = os.path.join("assets", "logo.png")

    # Draw Logo if exists
    if os.path.exists(logo_path):
        try:
            logo = ImageReader(logo_path)
            c.drawImage(logo, 50, height - 110, width=55, height=55, mask='auto')
        except Exception:
            # if logo file is broken, skip it
            pass

    c.setFont("Helvetica-Bold", 16)
    c.drawString(120, height - 70, company_name)

    c.setFont("Helvetica", 10)
    c.drawString(120, height - 88, company_tagline)

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "PAYSLIP")
    y -= 30

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Downloaded On: {downloaded_date}")
    y -= 18


    c.line(50, y, width - 50, y)
    y -= 25

    # Employee Details
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Employee Details")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Employee ID: {emp.id}")
    y -= 18
    c.drawString(50, y, f"Employee Code: {emp.emp_code}")
    y -= 18
    c.drawString(50, y, f"Name: {emp.full_name}")
    y -= 18
    c.drawString(50, y, f"Email: {emp.email}")
    y -= 18
    c.drawString(50, y, f"Department: {emp.department or '-'}")
    y -= 18
    c.drawString(50, y, f"Designation: {emp.designation or '-'}")
    y -= 30

    c.line(50, y, width - 50, y)
    y -= 25

    # Payroll Details
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Payroll Details")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Payroll ID: {payroll.id}")
    y -= 18
    month_name = calendar.month_name[payroll.month]
    c.drawString(50, y, f"Pay Period: {month_name} {payroll.year}")
    y -= 18
    c.drawString(50, y, f"Basic Salary: Rs. {float(payroll.basic_salary):.2f}")
    y -= 18
    c.drawString(50, y, f"Attendance: {payroll.days_present}/{payroll.total_working_days}")
    y -= 18

    y -= 10
    c.line(50, y, width - 50, y)
    y -= 25

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Earnings")
    c.drawString(320, y, "Deductions")
    y -= 18

    c.setFont("Helvetica", 11)

    # Earnings
    c.drawString(50, y, "Basic Salary")
    c.drawRightString(250, y, f"Rs. {float(payroll.basic_salary):.2f}")

    y -= 18
    c.drawString(50, y, "HRA (20%)")
    c.drawRightString(250, y, f"Rs. {float(payroll.hra):.2f}")

    y -= 18
    c.drawString(50, y, "DA (10%)")
    c.drawRightString(250, y, f"Rs. {float(payroll.da):.2f}")

    # Deductions
    y2 = y + 36
    c.drawString(320, y2, "PF (12%)")
    c.drawRightString(width - 50, y2, f"Rs. {float(payroll.pf):.2f}")

    # Gross + Net
    y -= 25
    gross = float(payroll.basic_salary) + float(payroll.hra) + float(payroll.da)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Gross Salary")
    c.drawRightString(250, y, f"Rs. {gross:.2f}")

    c.drawString(320, y, "Total Deductions")
    c.drawRightString(width - 50, y, f"Rs. {float(payroll.pf):.2f}")

    y -= 30
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, f"NET SALARY (after attendance): Rs. {float(payroll.net_salary):.2f}")

    #  move y down before writing notes
    y -= 22
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, y, "This payslip is system generated.")
    y -= 15
    c.drawString(50, y, "Signature not required.")
    y -= 10

    footer_y = 55
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, footer_y, "Generated by Payroll Management System (FastAPI + MySQL)")
    c.drawRightString(width - 50, footer_y, f"Generated: {downloaded_date}")

    c.showPage()
    c.save()

    buffer.seek(0)

    filename = f"Payslip_{emp.emp_code}_{payroll.month:02d}-{payroll.year}.pdf"

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )
