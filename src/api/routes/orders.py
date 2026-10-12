from fastapi import APIRouter
from sqlalchemy import text
from src.api.services.database import engine

router = APIRouter()

@router.get("/orders")
def get_orders():
    with engine.connect() as connection:
        result=connection.execute(
            text("""
                    SELECT
                        order_id,
                        order_item_id,
                        price,
                        freight_value,
                        shipping_limit_date
                    FROM fact_sales
                    ORDER BY shipping_limit_date DESC
                    LIMIT 20;
        """)
        )
        orders=[dict(row._mapping) for row in result.fetchall()]
    return orders
