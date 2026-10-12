from fastapi import APIRouter 
from src.api.services.database import engine
from sqlalchemy import text

router=APIRouter()

@router.get("/revenue")
def get_revenue():
    with engine.connect() as connection:
        result=connection.execute(
            text("""
                    SELECT SUM(total_sales)
                    FROM fact_sales;
                    """)
        )
        revenue=result.scalar()
    return {"revenue":revenue}

