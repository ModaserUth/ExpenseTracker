from sqlalchemy import Column, Integer, String, Float, Date
from database import Base
import datetime

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    amount = Column(Float)
    category = Column(String) # مثل: أكل، مواصلات، سكن
    date = Column(Date, default=datetime.date.today)

class Settings(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, index=True)
    monthly_income = Column(Float, default=20000.0)