from concurrent.futures import ProcessPoolExecutor

from src.logger import setup_logger

from src.analytics import (
    revenue_analysis,
    profit_analysis,
    customer_analysis,
    product_analysis,
    regional_analysis,
    revenue_forecast
)


logger = setup_logger()


class AnalyticsEngine:

    def __init__(
        self,
        orders,
        customers,
        products,
        returns
    ):

        self.orders = orders
        self.customers = customers
        self.products = products
        self.returns = returns

    def run_parallel_analysis(self):

        logger.info(
            "Starting Multiprocessing Analytics"
        )

        with ProcessPoolExecutor(
            max_workers=4
        ) as executor:

            revenue_future = executor.submit(
                revenue_analysis,
                self.orders
            )

            profit_future = executor.submit(
                profit_analysis,
                self.orders,
                self.products
            )

            customer_future = executor.submit(
                customer_analysis,
                self.orders
            )

            product_future = executor.submit(
                product_analysis,
                self.orders,
                self.products,
                self.returns
            )

            results = {

                "revenue":
                    revenue_future.result(),

                "profit":
                    profit_future.result(),

                "customer":
                    customer_future.result(),

                "product":
                    product_future.result()
            }

        logger.info(
            "Multiprocessing Analytics Complete"
        )

        return results

    def run_regional_analysis(self):

        logger.info(
            "Calculating Regional Performance"
        )

        return regional_analysis(
            self.orders,
            self.customers
        )

    def run_forecast(self):

        logger.info(
            "Calculating Revenue Forecast"
        )

        return revenue_forecast(
            self.orders
        )