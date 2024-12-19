import uvicorn
from fastapi import FastAPI
from routes.auth import auth_router
from routes.expense import expense_router

app = FastAPI()

app.include_router(router=auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(router=expense_router, prefix="/expenses", tags=["Expenses"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)