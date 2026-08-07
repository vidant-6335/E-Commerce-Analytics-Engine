import matplotlib.pyplot as plt
import seaborn as sns

from src.config import (
    REPORT_DIR,
    CHART_DIR
)

from src.logger import setup_logger


logger = setup_logger()


class ReportGenerator:

    def __init__(
        self,
        results,
        regional_data,
        forecast
    ):

        self.results = results
        self.regional_data = regional_data
        self.forecast = forecast

    def generate_summary(self):

        revenue = self.results[
            "revenue"
        ]

        profit = self.results[
            "profit"
        ]

        customer = self.results[
            "customer"
        ]

        summary = {

            "Total Revenue":
                revenue["total_revenue"],

            "Total Orders":
                revenue["total_orders"],

            "Average Order Value":
                revenue[
                    "average_order_value"
                ],

            "Total Profit":
                profit["total_profit"],

            "Profit Margin %":
                profit["profit_margin"],

            "Repeat Customers":
                customer[
                    "repeat_customers"
                ],

            "Retention Rate %":
                customer[
                    "retention_rate"
                ]
        }

        return summary

    def save_reports(self):

        logger.info(
            "Exporting Reports"
        )

        # Product report
        product_data = self.results[
            "product"
        ]

        product_data.to_csv(
            REPORT_DIR
            / "product_performance.csv",
            index=False
        )

        # Customer report
        customer_data = self.results[
            "customer"
        ]["customer_summary"]

        customer_data.to_csv(
            REPORT_DIR
            / "customer_analysis.csv",
            index=False
        )

        # Regional report
        self.regional_data.to_csv(
            REPORT_DIR
            / "regional_performance.csv",
            index=False
        )

        # Forecast
        self.forecast.to_csv(
            REPORT_DIR
            / "revenue_forecast.csv",
            index=False
        )

        # Summary
        summary = self.generate_summary()

        import pandas as pd

        pd.DataFrame(
            [summary]
        ).to_csv(
            REPORT_DIR
            / "executive_summary.csv",
            index=False
        )

        logger.info(
            "Reports Export Complete"
        )

    def build_charts(self):

        logger.info(
            "Building Charts"
        )

        # ------------------------
        # Regional Revenue
        # ------------------------

        plt.figure(figsize=(10, 6))

        sns.barplot(
            data=self.regional_data,
            x="region",
            y="revenue"
        )

        plt.title(
            "Revenue by Region"
        )

        plt.xticks(rotation=45)

        plt.tight_layout()

        plt.savefig(
            CHART_DIR
            / "regional_revenue.png"
        )

        plt.close()

        # ------------------------
        # Top Products
        # ------------------------

        top_products = (
            self.results["product"]
            .nlargest(
                10,
                "revenue"
            )
        )

        plt.figure(figsize=(12, 6))

        sns.barplot(
            data=top_products,
            x="product_name",
            y="revenue"
        )

        plt.title(
            "Top 10 Products by Revenue"
        )

        plt.xticks(
            rotation=45,
            ha="right"
        )

        plt.tight_layout()

        plt.savefig(
            CHART_DIR
            / "top_products.png"
        )

        plt.close()

        # ------------------------
        # Revenue Forecast
        # ------------------------

        if not self.forecast.empty:

            plt.figure(figsize=(12, 6))

            plt.plot(
                self.forecast["date"],
                self.forecast[
                    "forecast_revenue"
                ]
            )

            plt.title(
                "Revenue Forecast"
            )

            plt.xlabel("Date")

            plt.ylabel(
                "Forecast Revenue"
            )

            plt.tight_layout()

            plt.savefig(
                CHART_DIR
                / "revenue_forecast.png"
            )

            plt.close()

        logger.info(
            "Chart Generation Complete"
        )