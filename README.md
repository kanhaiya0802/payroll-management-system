# payroll-management-system
Payroll Management System using FastAPI + MySQL with Admin/Employee role-based access and PDF payslip download.
---

## 🚀 Features

### ✅ Authentication & Role-Based Access
- JWT based login system
- Role-based access control:
  - **Admin**: full access
  - **Employee**: limited access (only own profile & payslips)

### ✅ Admin Module
- Add employee
- View employee list
- Mark monthly attendance
- Generate payroll based on attendance
- Create employee login (temporary password)
- Delete employee
- View payroll history
- Download any employee payslip PDF

### ✅ Employee Module
- Login securely
- View own employee profile
- View own generated payslips
- Download payslip as PDF

### ✅ Professional Payslip PDF
- Includes:
  - Company name + logo
  - Pay period
  - Employee details
  - Earnings & deductions breakdown (Basic, HRA, DA, PF)
  - Net salary
  - Download timestamp

### ✅ Security Feature
- **Force Change Password** on first login:
  - Admin assigns temporary password
  - Employee must change password after login

---

## 🛠️ Tech Stack

**Frontend**
- HTML, CSS, JavaScript

**Backend**
- Python (FastAPI)
- SQLAlchemy ORM

**Database**
- MySQL

---

## 📁 Project Structure

```txt
PayrollManagement/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── dependencies.py
│   ├── routes/
│   │   ├── employee.py
│   │   ├── attendance.py
│   │   ├── payroll.py
│   │   └── payslip_pdf.py
│   └── assets/
│       └── logo.png
│
└── frontend/
    ├── login.html
    ├── admin_dashboard.html
    ├── employee_dashboard.html
    ├── add_employee.html
    ├── view_employees.html
    ├── mark_attendance.html
    ├── generate_payroll.html
    ├── create_employee_login.html
    ├── employee_profile.html
    ├── employee_payslips.html
    ├── admin_payroll_history.html
    ├── change_password.html
    ├── css/
    │   └── style.css
    └── js/
        ├── common.js
        └── login.js
```

## ✅ Installation & Setup

### 1️⃣ Clone repository
```bash
git clone https://github.com/<your-username>/payroll-management-system.git
cd payroll-management-system
```
### 2️⃣ Backend Setup (FastAPI)
Go inside backend folder:
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```
Install dependencies:
```bash
pip install -r requirements.txt
```
### 3️⃣ MySQL Setup
Create database:
```bash
CREATE DATABASE payroll_db;
USE payroll_db;
```
Update .env file inside backend:
```bash
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=payroll_db
DB_PORT=3306
```
### 4️⃣ Run Backend
```bash
python -m uvicorn main:app --reload
```
Backend running at:
📌 http://127.0.0.1:8000

Swagger Docs:
📌 http://127.0.0.1:8000/docs

### 5️⃣ Run Frontend
Open frontend/login.html using VS Code Live Server.

---

## 🔑 User Roles & Flow
### ✅ Admin

Add employee
Create employee login (temporary password)
Attendance → Payroll generation → Payslip download

### ✅ Employee

Login using temporary password
First login → must change password
View profile + payslips
Download payslip PDF

---

## ✨ Future Enhancements
Edit employee details
Search/filter employees
Email payslip feature
Payslip zip download
Deploy on cloud (Render/Railway)

---

## 👩‍💻 Developer
Name: Kanhaiya Jee
Role: B.Tech IT Student
Project Type: Full Stack Web Application

---

## 📜 License
This project is for learning and educational purposes.
