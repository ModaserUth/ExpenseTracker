from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas
from database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# جلب كل المصاريف
@app.get("/expenses", response_model=list[schemas.ExpenseResponse])
def get_expenses(db: Session = Depends(get_db)):
    return db.query(models.Expense).order_by(models.Expense.id.desc()).all()

# إضافة مصروف
@app.post("/add-expense", response_model=schemas.ExpenseResponse)
def add_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = models.Expense(**expense.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

# حذف مصروف واحد
@app.delete("/delete-expense/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="غير موجود")
    db.delete(expense)
    db.commit()
    return {"status": "success"}

# حذف الكل (تصفير)
@app.delete("/reset-all")
def reset_all(db: Session = Depends(get_db)):
    db.query(models.Expense).delete()
    db.commit()
    return {"status": "success"}

# تعديل مصروف
@app.put("/update-expense/{expense_id}")
def update_expense(expense_id: int, expense_data: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="غير موجود")
    db_expense.title = expense_data.title
    db_expense.amount = expense_data.amount
    db_expense.category = expense_data.category
    db.commit()
    return {"status": "success"}

@app.get("/report")
def get_report(db: Session = Depends(get_db)):
    settings = db.query(models.Settings).first()
    income = settings.monthly_income if settings else 20000.0
    total_spent = db.query(func.sum(models.Expense.amount)).scalar() or 0.0
    return {"total_income": income, "total_expenses": total_spent, "remaining_balance": income - total_spent}

@app.post("/update-income")
def update_income(amount: float, db: Session = Depends(get_db)):
    settings = db.query(models.Settings).first()
    if not settings:
        settings = models.Settings(monthly_income=amount)
        db.add(settings)
    else:
        settings.monthly_income = amount
    db.commit()
    return {"status": "success"}

@app.get("/chart-data")
def get_chart_data(db: Session = Depends(get_db)):
    res = db.query(models.Expense.category, func.sum(models.Expense.amount)).group_by(models.Expense.category).all()
    return {"labels": [r[0] for r in res], "data": [r[1] for r in res]}

@app.get("/")
async def read_index():
    path = os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html")
    return FileResponse(path)