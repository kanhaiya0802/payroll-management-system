print("✅ NEW MAIN.PY LOADED WITH REGISTER/LOGIN")
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from schemas import RegisterRequest, LoginRequest
from models import User
from auth import hash_password, verify_password, create_access_token
from fastapi import HTTPException
from dependencies import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from routes.employee import router as employee_router
from routes.employee_self import router as employee_self_router

from routes.attendance import router as attendance_router
from routes.payroll import router as payroll_router

from database import get_db, engine
import models

from fastapi.middleware.cors import CORSMiddleware

from routes.payslip_pdf import router as payslip_pdf_router
from schemas import ChangePasswordRequest
from auth import hash_password, verify_password
from datetime import datetime


# if tables not exist 
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Payroll Management System")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employee_router)
app.include_router(employee_self_router)

app.include_router(attendance_router)
app.include_router(payroll_router)
app.include_router(payslip_pdf_router)


@app.get("/")
def home():
    return {"message": "Payroll backend running ✅"}

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT DATABASE();")).fetchone()
    return {"connected_database": result[0]}

@app.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        full_name=data.full_name,
        email=data.email,
        password_hash=hash_password(data.password),
        role=data.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered successfully ✅", "role": user.role}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"user_id": user.id, "role": user.role})

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "must_change_password": user.must_change_password
    }


@app.get("/me")
def read_me(user=Depends(get_current_user)):
    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role
    }

@app.post("/change-password")
def change_password(
    data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # verify old password
    if not verify_password(data.old_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    # basic validation
    if len(data.new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    user.password_hash = hash_password(data.new_password)
    user.must_change_password = False
    user.password_changed_at = datetime.now()

    db.commit()

    return {"message": "Password changed successfully ✅"}