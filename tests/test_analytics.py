import pandas as pd

from src.analytics import (
    revenue_analysis
)


def test_revenue_analysis():

    orders = pd.DataFrame({

        "order_id": [
            "O1",
            "O2"
        ],

        "quantity": [
            2,
            3
        ],

        "unit_price": [
            100,
            200
        ],

        "order_date": pd.to_datetime([
            "2025-01-01",
            "2025-01-02"
        ])
    })

    result = revenue_analysis(
        orders
    )

    assert result[
        "total_revenue"
    ] == 800