from fastapi import FastAPI
from src.api.routes.revenue import router as revenue_router
from src.api.routes.products import router as products_router
from src.api.routes.customers import router as customers_router
from src.api.routes.orders import router as orders_router

# test with python -m uvicorn src.api.main:app --reload
# go to http://127.0.0.1:8000/docs

app=FastAPI()

app.include_router(revenue_router)
app.include_router(products_router)
app.include_router(customers_router)
app.include_router(orders_router)
#FastAPI, add all the endpoints defined inside this router to my application.


