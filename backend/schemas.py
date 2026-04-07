from pydantic import BaseModel
import datetime
from typing import List, Dict

class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category: str
    date: datetime.date = datetime.date.today()

class ExpenseResponse(ExpenseCreate):
    id: int
    class Config:
        from_attributes = True

class ReportResponse(BaseModel):
    total_income: float
    total_expenses: float
    remaining_balance: float

class ChartDataResponse(BaseModel):
    labels: List[str] # الفئات
    data: List[float] # المبالغ