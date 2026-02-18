from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("MYSQL_URL")

# 🚨 DEBUG PRINT (will appear in Railway logs)
print("DATABASE_URL from env:", DATABASE_URL)

# ⭐ FALLBACK if Railway variable missing
if not DATABASE_URL:
    DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/test"
    print("⚠️ USING FALLBACK DB URL")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()