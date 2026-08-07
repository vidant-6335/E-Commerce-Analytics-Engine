import pandas as pd
import numpy as np


def revenue_analysis(orders):

    orders = orders.copy()

    orders["revenue"] = (
        orders["quantity"]
        * orders["unit_price"]
    )

    total_revenue = orders["revenue"].sum()

    total_orders = orders["order_id"].nunique()

    average_order_value = (
        total_revenue / total_orders
        if total_orders
        else 0
    )

    daily_sales = (
        orders
        .groupby(
            "order_date"
        )["revenue"]
        .sum()
        .reset_index()
    )

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "average_order_value":
            average_order_value,
        "daily_sales": daily_sales
    }


def profit_analysis(
    orders,
    products
):

    df = orders.merge(
        products[
            [
                "product_id",
                "cost_price"
            ]
        ],
        on="product_id",
        how="left"
    )

    df["revenue"] = (
        df["quantity"]
        * df["unit_price"]
    )

    df["cost"] = (
        df["quantity"]
        * df["cost_price"]
    )

    df["profit"] = (
        df["revenue"]
        - df["cost"]
    )

    total_profit = df["profit"].sum()

    profit_margin = (
        total_profit
        / df["revenue"].sum()
        * 100
        if df["revenue"].sum()
        else 0
    )

    return {
        "total_profit": total_profit,
        "profit_margin": profit_margin,
        "profit_data": df
    }

def customer_analysis(orders):

    orders = orders.copy()

    orders["revenue"] = (
        orders["quantity"]
        * orders["unit_price"]
    )

    customer_summary = (
        orders
        .groupby("customer_id")
        .agg(
            orders=("order_id", "nunique"),
            revenue=("revenue", "sum"),
            quantity=("quantity", "sum")
        )
        .reset_index()
    )

    repeat_customers = (
        customer_summary[
            customer_summary["orders"] > 1
        ]
    )

    total_customers = len(
        customer_summary
    )

    retention_rate = (
        len(repeat_customers)
        / total_customers
        * 100
        if total_customers
        else 0
    )

    return {
        "customer_summary":
            customer_summary,
        "repeat_customers":
            len(repeat_customers),
        "retention_rate":
            retention_rate
    }


def product_analysis(
    orders,
    products,
    returns
):

    df = orders.merge(
        products[
            [
                "product_id",
                "product_name",
                "category",
                "cost_price"
            ]
        ],
        on="product_id",
        how="left"
    )

    df["revenue"] = (
        df["quantity"]
        * df["unit_price"]
    )

    df["profit"] = (
        df["quantity"]
        * (
            df["unit_price"]
            - df["cost_price"]
        )
    )

    product_summary = (
        df
        .groupby(
            [
                "product_id",
                "product_name",
                "category"
            ]
        )
        .agg(
            quantity_sold=(
                "quantity",
                "sum"
            ),
            revenue=(
                "revenue",
                "sum"
            ),
            profit=(
                "profit",
                "sum"
            )
        )
        .reset_index()
    )

    return_summary = (
        returns
        .groupby("product_id")
        ["quantity_returned"]
        .sum()
        .reset_index()
    )

    return_summary.rename(
        columns={
            "quantity_returned":
                "returned_quantity"
        },
        inplace=True
    )

    product_summary = product_summary.merge(
        return_summary,
        on="product_id",
        how="left"
    )

    product_summary[
        "returned_quantity"
    ] = product_summary[
        "returned_quantity"
    ].fillna(0)

    product_summary["return_rate"] = (
        product_summary["returned_quantity"]
        / product_summary["quantity_sold"]
        * 100
    )

    return product_summary

def regional_analysis(
    orders,
    customers
):

    df = orders.merge(
        customers[
            [
                "customer_id",
                "region"
            ]
        ],
        on="customer_id",
        how="left"
    )

    df["revenue"] = (
        df["quantity"]
        * df["unit_price"]
    )

    regional = (
        df
        .groupby("region")
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
            customers=(
                "customer_id",
                "nunique"
            )
        )
        .reset_index()
    )

    return regional


def revenue_forecast(
    orders,
    periods=30
):

    df = orders.copy()

    df["revenue"] = (
        df["quantity"]
        * df["unit_price"]
    )

    daily = (
        df
        .groupby("order_date")
        ["revenue"]
        .sum()
        .reset_index()
        .sort_values("order_date")
    )

    daily["day_number"] = np.arange(
        len(daily)
    )

    x = daily["day_number"].values
    y = daily["revenue"].values

    if len(x) < 2:
        return pd.DataFrame()

    slope, intercept = np.polyfit(
        x,
        y,
        1
    )

    future_x = np.arange(
        len(daily),
        len(daily) + periods
    )

    predictions = (
        slope * future_x
        + intercept
    )

    future_dates = pd.date_range(
        daily["order_date"].max()
        + pd.Timedelta(days=1),
        periods=periods
    )

    forecast = pd.DataFrame({
        "date": future_dates,
        "forecast_revenue":
            np.maximum(predictions, 0)
    })

    return forecast