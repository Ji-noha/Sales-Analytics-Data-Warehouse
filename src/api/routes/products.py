from fastapi import APIRouter
from sqlalchemy import text
from src.api.services.database import engine

router = APIRouter()

@router.get("/top-products")
def get_top_products():
    with engine.connect() as connection:
        result=connection.execute(
            text("""
                    SELECT
                        p.product_id,
                        SUM(f.total_sales) AS revenue
                    FROM fact_sales f
                    JOIN dim_product p
                        ON f.product_key = p.product_key
                    GROUP BY p.product_id
                    ORDER BY revenue DESC
                    LIMIT 10;
        """)
        )
        top_products=[dict(row._mapping) for row in result.fetchall()]
    return top_products
