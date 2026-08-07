from dataclasses import dataclass
from datetime import datetime


@dataclass
class Product:

    product_id: str
    product_name: str
    category: str
    price: float
    cost_price: float
    seller_id: str

    @property
    def profit_margin(self):

        if self.price == 0:
            return 0

        return (
            (self.price - self.cost_price)
            / self.price
        ) * 100


@dataclass
class Customer:

    customer_id: str
    customer_name: str
    region: str
    age: int


@dataclass
class Order:

    order_id: str
    customer_id: str
    product_id: str
    seller_id: str
    order_date: datetime
    quantity: int
    unit_price: float

    @property
    def revenue(self):

        return self.quantity * self.unit_price


@dataclass
class Seller:

    seller_id: str
    seller_name: str