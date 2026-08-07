import os
import numpy as np
import pandas as pd


np.random.seed(42)

RAW_DATA_PATH = "data/raw"

os.makedirs(RAW_DATA_PATH, exist_ok=True)


# -----------------------------
# CONFIGURATION
# -----------------------------

NUM_CUSTOMERS = 10000
NUM_PRODUCTS = 1000
NUM_SELLERS = 200
NUM_ORDERS = 100000
NUM_RETURNS = 8000


# -----------------------------
# SELLERS
# -----------------------------

sellers = pd.DataFrame({
    "seller_id": [f"S{i:04d}" for i in range(1, NUM_SELLERS + 1)],
    "seller_name": [
        f"Seller_{i}" for i in range(1, NUM_SELLERS + 1)
    ]
})

sellers.to_csv(
    f"{RAW_DATA_PATH}/sellers.csv",
    index=False
)


# -----------------------------
# PRODUCTS
# -----------------------------

categories = [
    "Electronics",
    "Fashion",
    "Home",
    "Beauty",
    "Sports",
    "Books",
    "Grocery",
    "Toys"
]

products = pd.DataFrame({
    "product_id": [
        f"P{i:05d}" for i in range(1, NUM_PRODUCTS + 1)
    ],
    "product_name": [
        f"Product_{i}" for i in range(1, NUM_PRODUCTS + 1)
    ],
    "category": np.random.choice(
        categories,
        NUM_PRODUCTS
    ),
    "price": np.round(
        np.random.uniform(100, 50000, NUM_PRODUCTS),
        2
    ),
    "cost_price": np.round(
        np.random.uniform(50, 35000, NUM_PRODUCTS),
        2
    ),
    "seller_id": np.random.choice(
        sellers["seller_id"],
        NUM_PRODUCTS
    )
})

# Make sure cost < selling price
products["cost_price"] = np.minimum(
    products["cost_price"],
    products["price"] * 0.8
)

products.to_csv(
    f"{RAW_DATA_PATH}/products.csv",
    index=False
)


# -----------------------------
# CUSTOMERS
# -----------------------------

regions = [
    "North",
    "South",
    "East",
    "West",
    "Central"
]

customers = pd.DataFrame({
    "customer_id": [
        f"C{i:06d}" for i in range(1, NUM_CUSTOMERS + 1)
    ],
    "customer_name": [
        f"Customer_{i}" for i in range(1, NUM_CUSTOMERS + 1)
    ],
    "region": np.random.choice(
        regions,
        NUM_CUSTOMERS
    ),
    "age": np.random.randint(
        18,
        65,
        NUM_CUSTOMERS
    )
})

customers.to_csv(
    f"{RAW_DATA_PATH}/customers.csv",
    index=False
)


# -----------------------------
# ORDERS
# -----------------------------

order_dates = pd.date_range(
    start="2024-01-01",
    end="2025-12-31"
)

orders = pd.DataFrame({
    "order_id": [
        f"O{i:07d}" for i in range(1, NUM_ORDERS + 1)
    ],
    "customer_id": np.random.choice(
        customers["customer_id"],
        NUM_ORDERS
    ),
    "product_id": np.random.choice(
        products["product_id"],
        NUM_ORDERS
    ),
    "seller_id": np.random.choice(
        sellers["seller_id"],
        NUM_ORDERS
    ),
    "order_date": np.random.choice(
        order_dates,
        NUM_ORDERS
    ),
    "quantity": np.random.randint(
        1,
        6,
        NUM_ORDERS
    )
})

# Attach product price
price_map = products.set_index("product_id")["price"]

orders["unit_price"] = orders["product_id"].map(price_map)

orders["unit_price"] = orders["unit_price"].fillna(
    orders["unit_price"].median()
)

orders.to_csv(
    f"{RAW_DATA_PATH}/orders.csv",
    index=False
)


# -----------------------------
# RETURNS
# -----------------------------

return_orders = np.random.choice(
    orders["order_id"],
    NUM_RETURNS,
    replace=False
)

returns = orders[
    orders["order_id"].isin(return_orders)
][[
    "order_id",
    "product_id"
]].copy()

returns["return_id"] = [
    f"R{i:07d}" for i in range(1, len(returns) + 1)
]

returns["return_date"] = pd.to_datetime(
    orders.set_index("order_id")
    .loc[returns["order_id"], "order_date"]
).values

returns["quantity_returned"] = np.random.randint(
    1,
    3,
    len(returns)
)

returns["reason"] = np.random.choice(
    [
        "Damaged",
        "Wrong Product",
        "Changed Mind",
        "Late Delivery",
        "Quality Issue"
    ],
    len(returns)
)

returns = returns[
    [
        "return_id",
        "order_id",
        "product_id",
        "return_date",
        "quantity_returned",
        "reason"
    ]
]

returns.to_csv(
    f"{RAW_DATA_PATH}/returns.csv",
    index=False
)


print("Dataset generation completed.")
print(f"Customers : {len(customers):,}")
print(f"Products  : {len(products):,}")
print(f"Sellers   : {len(sellers):,}")
print(f"Orders    : {len(orders):,}")
print(f"Returns   : {len(returns):,}")