from fastapi import Depends, APIRouter, HTTPException, status
from database import expense_colection
from models import Expense, DateRange, ExpenseId
from utils import get_current_user

expense_router = APIRouter()

@expense_router.post("/expenses", status_code=status.HTTP_201_CREATED)
async def create_expense(expense : Expense, user: str = Depends(get_current_user)):
    try:
        if not isinstance(expense.amount, float):
            raise HTTPException(status_code=400, detail={"message" : "Invalid amount type"})
        
        if not isinstance(expense.category, str) or not isinstance(expense.description, str):
            raise HTTPException(status_code=400, detail={"message" : "Invalid category and description type"})


        expense_data = {
            "username" : user["username"],
            "amount": expense.amount,
            "category": expense.category,
            "description": expense.description,
            "date" : expense.date.isoformat()
        }


        expense_obj = expense_colection.insert_one(expense_data)
        expense_id = str(expense_obj.inserted_id)
        return {"message" : "Creation successfull", "expenseId" : expense_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"message" : f"{e}"})
    
    
@expense_router.get("/expenses/filter", status_code=status.HTTP_200_OK)
async def filter_expenses(date_range : DateRange, user: str = Depends(get_current_user)):
    try:
        if not date_range.start_date or not date_range.end_date:
            raise HTTPException(status_code=400, detail={"message" : "range not provided"})
        
        expenses = expense_colection.find({
            "username" : user["username"],
            "date" : {
                "$gte" : date_range.start_date.isoformat(),
                "$lte" : date_range.end_date.isoformat()
            }
        })

        expenses_list = []

        for doc in expenses.to_list():
            doc["_id"] = str(doc["_id"])
            expenses_list.append(doc)
        

        if not expenses_list:
            raise HTTPException(status_code=404, detail={"message" : "No data found"})
    
        return expenses_list
    except Exception as e:
            raise HTTPException(status_code=500, detail={"message" : f"{e}"})


