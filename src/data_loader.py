import pandas as pd
from concurrent.futures import ThreadPoolExecutor

from src.logger import setup_logger


logger = setup_logger()


def optimize_dataframe(df):

    for column in df.columns:

        if df[column].dtype == "object":

            # Convert low-cardinality strings
            unique_ratio = (
                df[column].nunique(dropna=False)
                / len(df)
            )

            if unique_ratio < 0.5:
                df[column] = df[column].astype(
                    "category"
                )

    # Downcast integers
    integer_columns = df.select_dtypes(
        include=["int64", "int32"]
    ).columns

    for column in integer_columns:

        df[column] = pd.to_numeric(
            df[column],
            downcast="integer"
        )

    # Downcast floats
    float_columns = df.select_dtypes(
        include=["float64"]
    ).columns

    for column in float_columns:

        df[column] = pd.to_numeric(
            df[column],
            downcast="float"
        )

    return df


def load_csv(
    file_path,
    parse_dates=None,
    chunksize=10000
):

    logger.info(
        f"Loading {file_path.name}"
    )

    chunks = []

    for chunk in pd.read_csv(
        file_path,
        parse_dates=parse_dates,
        chunksize=chunksize
    ):

        chunk = optimize_dataframe(chunk)

        chunks.append(chunk)

    df = pd.concat(
        chunks,
        ignore_index=True
    )

    logger.info(
        f"Loaded {file_path.name}: "
        f"{len(df):,} rows"
    )

    return df


def load_all_data(paths):

    with ThreadPoolExecutor(
        max_workers=4
    ) as executor:

        futures = {

            "orders": executor.submit(
                load_csv,
                paths["orders"],
                ["order_date"]
            ),

            "customers": executor.submit(
                load_csv,
                paths["customers"]
            ),

            "products": executor.submit(
                load_csv,
                paths["products"]
            ),

            "returns": executor.submit(
                load_csv,
                paths["returns"],
                ["return_date"]
            )
        }

        data = {
            name: future.result()
            for name, future in futures.items()
        }

    return data


    

def memory_usage(df):

    memory = df.memory_usage(
        deep=True
    ).sum()

    return memory / 1024 ** 2

print(
    f"Memory: {memory_usage(df):.2f} MB"
)

