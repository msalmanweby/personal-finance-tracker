from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class User(BaseModel):
    username: str
    password : str

class TokenData(BaseModel):
    username: str | None = None

class UserInDB(User):
    hashed_password: str

class Expense(BaseModel):
    amount: float
    category: str
    description: str
    date : date

class DateRange(BaseModel):
    start_date: date
    end_date: date

class ExpenseId(BaseModel):
    _id: str