import pandas as pd

from config.config import SALES_DATA_FILE


def extract_sales_data() -> pd.DataFrame:
    """
    Read the raw Superstore CSV file and return the data as a DataFrame.

    Returns:
        pd.DataFrame: Raw sales data.
    """
    return pd.read_csv(SALES_DATA_FILE)


if __name__ == "__main__":
    sales_data = extract_sales_data()

    print(f"Rows extracted: {len(sales_data)}")
    print(f"Columns extracted: {len(sales_data.columns)}")