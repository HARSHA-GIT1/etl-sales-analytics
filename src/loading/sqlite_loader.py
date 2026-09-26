import sqlite3

import pandas as pd

from config.config import DATABASE_FILE


def load_sales_data(
    sales_data: pd.DataFrame,
) -> None:
    """
    Load transformed sales data into a SQLite database.

    Args:
        sales_data: Validated transformed sales DataFrame.
    """
    DATABASE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(DATABASE_FILE)

    try:
        sales_data.to_sql(
            "sales",
            connection,
            if_exists="replace",
            index=False,
        )
    finally:
        connection.close()


if __name__ == "__main__":
    from src.extraction.csv_extractor import extract_sales_data
    from src.extraction.api_extractor import extract_exchange_rate
    from src.transformation.sales_transformer import transform_sales_data
    from src.validation.data_validator import validate_sales_data

    sales_data = extract_sales_data()

    exchange_data = extract_exchange_rate()
    exchange_rate = exchange_data["rates"]["INR"]

    transformed_data = transform_sales_data(
        sales_data,
        exchange_rate,
    )

    validation_results = validate_sales_data(transformed_data)

    if not validation_results["is_valid"]:
        raise ValueError(
            "Data validation failed. Database load stopped."
        )

    load_sales_data(transformed_data)

    print(f"Database created: {DATABASE_FILE}")
    print(f"Rows loaded: {len(transformed_data)}")