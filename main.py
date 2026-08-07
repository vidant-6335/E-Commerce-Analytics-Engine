import gc

from src.config import (
    ORDERS_FILE,
    CUSTOMERS_FILE,
    PRODUCTS_FILE,
    RETURNS_FILE
)

from src.logger import setup_logger

from src.data_loader import (
    load_all_data
)

from src.data_cleaner import (
    clean_all
)

from src.engine import (
    AnalyticsEngine
)

from src.report_generator import (
    ReportGenerator
)


def main():

    logger = setup_logger()

    logger.info(
        "===================================="
    )

    logger.info(
        "E-COMMERCE ANALYTICS ENGINE STARTED"
    )

    logger.info(
        "===================================="
    )

    # --------------------------------
    # 1. LOAD DATA
    # --------------------------------

    paths = {

        "orders": ORDERS_FILE,

        "customers":
            CUSTOMERS_FILE,

        "products":
            PRODUCTS_FILE,

        "returns":
            RETURNS_FILE
    }

    data = load_all_data(paths)

    # --------------------------------
    # 2. CLEAN DATA
    # --------------------------------

    data = clean_all(data)

    # --------------------------------
    # 3. CREATE ENGINE
    # --------------------------------

    engine = AnalyticsEngine(
        orders=data["orders"],
        customers=data["customers"],
        products=data["products"],
        returns=data["returns"]
    )

    # --------------------------------
    # 4. MULTIPROCESSING
    # --------------------------------

    results = (
        engine.run_parallel_analysis()
    )

    # --------------------------------
    # 5. REGIONAL ANALYSIS
    # --------------------------------

    regional_data = (
        engine.run_regional_analysis()
    )

    # --------------------------------
    # 6. FORECAST
    # --------------------------------

    forecast = (
        engine.run_forecast()
    )

    # --------------------------------
    # 7. REPORT GENERATION
    # --------------------------------

    generator = ReportGenerator(
        results,
        regional_data,
        forecast
    )

    generator.save_reports()

    generator.build_charts()

    # --------------------------------
    # 8. CLEAN MEMORY
    # --------------------------------

    del data

    gc.collect()

    logger.info(
        "===================================="
    )

    logger.info(
        "E-COMMERCE ANALYTICS ENGINE COMPLETE"
    )

    logger.info(
        "===================================="
    )


if __name__ == "__main__":

    main()