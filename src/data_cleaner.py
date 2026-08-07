import gc

from src.logger import setup_logger


logger = setup_logger()


def clean_orders(df):

    logger.info("Cleaning Orders Dataset")

    df = df.drop_duplicates()

    df = df.dropna(
        subset=[
            "order_id",
            "customer_id",
            "product_id",
            "order_date"
        ]
    )

    df["quantity"] = df["quantity"].clip(
        lower=1
    )

    df["unit_price"] = df["unit_price"].clip(
        lower=0
    )

    return df


def clean_customers(df):

    logger.info("Cleaning Customers Dataset")

    df = df.drop_duplicates()

    df = df.dropna(
        subset=["customer_id"]
    )

    return df


def clean_products(df):

    logger.info("Cleaning Products Dataset")

    df = df.drop_duplicates()

    df = df.dropna(
        subset=["product_id"]
    )

    df["price"] = df["price"].clip(
        lower=0
    )

    df["cost_price"] = df["cost_price"].clip(
        lower=0
    )

    return df


def clean_returns(df):

    logger.info("Cleaning Returns Dataset")

    df = df.drop_duplicates()

    df["quantity_returned"] = (
        df["quantity_returned"].clip(lower=1)
    )

    return df


def clean_all(data):

    data["orders"] = clean_orders(
        data["orders"]
    )

    data["customers"] = clean_customers(
        data["customers"]
    )

    data["products"] = clean_products(
        data["products"]
    )

    data["returns"] = clean_returns(
        data["returns"]
    )

    gc.collect()

    logger.info("Dataset Cleaning Complete")

    return data