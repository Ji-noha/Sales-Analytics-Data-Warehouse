from fastapi import APIRouter
from sqlalchemy import text
from src.api.services.database import engine

router = APIRouter()

@router.get("/top-customers")
def get_top_customers():
    with engine.connect() as connection:
        result=connection.execute(
            text("""
                    SELECT
                        c.customer_id,
                        SUM(f.total_sales) AS revenue
                    FROM fact_sales f
                    JOIN dim_customer c
                        ON f.customer_key = c.customer_key
                    GROUP BY c.customer_id
                    ORDER BY revenue DESC
                    LIMIT 10;
                """)
        )
        top_customers=[dict(row._mapping) for row in result.fetchall()]
    return top_customers
