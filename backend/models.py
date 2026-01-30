from sqlalchemy import Column, Integer, String, Enum, Date, DECIMAL, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from database import Base
from sqlalchemy import ForeignKey
from sqlalchemy import Boolean, DateTime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum("admin", "employee"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True, unique=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    must_change_password = Column(Boolean, default=False)
    password_changed_at = Column(DateTime, nullable=True)


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    emp_code = Column(String(20), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15))
    designation = Column(String(50))
    department = Column(String(50))
    basic_salary = Column(DECIMAL(10, 2), nullable=False, default=0)
    joining_date = Column(Date)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    days_present = Column(Integer, nullable=False, default=0)
    total_working_days = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())

    __table_args__ = (UniqueConstraint("employee_id", "month", "year", name="uq_attendance"),)


class Payroll(Base):
    __tablename__ = "payroll"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

    basic_salary = Column(DECIMAL(10, 2), nullable=False)
    days_present = Column(Integer, nullable=False)
    total_working_days = Column(Integer, nullable=False)
    net_salary = Column(DECIMAL(10, 2), nullable=False)
    hra = Column(DECIMAL(10,2), nullable=False, default=0)
    da = Column(DECIMAL(10,2), nullable=False, default=0)
    pf = Column(DECIMAL(10,2), nullable=False, default=0)

    generated_at = Column(TIMESTAMP, server_default=func.now())

    __table_args__ = (UniqueConstraint("employee_id", "month", "year", name="uq_payroll"),)
