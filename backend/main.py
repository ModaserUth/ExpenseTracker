from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas
from database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware

# إضافات الربط مع ملفات الواجهة
from fastapi.responses import FileResponse
import os

# إنشاء الجداول في قاعدة البيانات
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# --- الـ Endpoints الخاصة بالبيانات ---

@app.post("/add-expense", response_model=schemas.ExpenseResponse)
def add_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = models.Expense(**expense.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@app.get("/report", response_model=schemas.ReportResponse)
def get_report(db: Session = Depends(get_db)):
    settings = db.query(models.Settings).first()
    income = settings.monthly_income if settings else 20000.0
    total_spent = db.query(func.sum(models.Expense.amount)).scalar() or 0.0
    return {
        "total_income": income,
        "total_expenses": total_spent,
        "remaining_balance": income - total_spent
    }

@app.get("/chart-data", response_model=schemas.ChartDataResponse)
def get_chart_data(db: Session = Depends(get_db)):
    results = db.query(
        models.Expense.category, 
        func.sum(models.Expense.amount)
    ).group_by(models.Expense.category).all()
    labels = [row[0] for row in results]
    data = [row[1] for row in results]
    return {"labels": labels, "data": data}

# --- التعديل الجديد لربط الـ Frontend ---
# هذا المسار يجعل المتصفح يفتح صفحة index.html عند الدخول على الرابط الأساسي http://127.0.0.1:8000/

@app.get("/")
async def read_index():
    # نحدد مسار ملف index.html بالخروج من مجلد backend ثم الدخول لمجلد frontend
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html")
    return FileResponse(frontend_path)