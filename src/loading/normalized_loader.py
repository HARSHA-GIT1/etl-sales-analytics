import sqlite3

import pandas as pd

from config.config import DATABASE_FILE


def load_normalized_data(sales_data: pd.DataFrame) -> None:
    """
    Load transformed sales data into the normalized SQLite tables.

    Args:
        sales_data: Validated transformed sales DataFrame.
    """
    connection = sqlite3.connect(DATABASE_FILE)

    try:
        connection.execute("PRAGMA foreign_keys = ON")

        # Customers
        customers = sales_data[
            [
                "Customer ID",
                "Customer Name",
                "Segment",
            ]
        ].drop_duplicates(subset=["Customer ID"])

        customers = customers.rename(
            columns={
                "Customer ID": "customer_id",
                "Customer Name": "customer_name",
                "Segment": "segment",
            }
        )

        customers.to_sql(
            "customers",
            connection,
            if_exists="append",
            index=False,
        )

        # Products
        products = sales_data[
            [
                "Product ID",
                "Product Name",
                "Category",
                "Sub-Category",
            ]
        ].drop_duplicates(subset=["Product ID"])

        products = products.rename(
            columns={
                "Product ID": "product_id",
                "Product Name": "product_name",
                "Category": "category",
                "Sub-Category": "sub_category",
            }
        )

        products.to_sql(
            "products",
            connection,
            if_exists="append",
            index=False,
        )

        # Orders
        orders = sales_data[
            [
                "Order ID",
                "Order Date",
                "Ship Date",
                "Ship Mode",
                "Customer ID",
                "Country/Region",
                "City",
                "State/Province",
                "Postal Code",
                "Region",
            ]
        ].drop_duplicates(subset=["Order ID"])

        orders = orders.rename(
            columns={
                "Order ID": "order_id",
                "Order Date": "order_date",
                "Ship Date": "ship_date",
                "Ship Mode": "ship_mode",
                "Customer ID": "customer_id",
                "Country/Region": "country",
                "City": "city",
                "State/Province": "state",
                "Postal Code": "postal_code",
                "Region": "region",
            }
        )

        # SQLite stores dates as text.
        orders["order_date"] = orders["order_date"].dt.strftime(
            "%Y-%m-%d"
        )

        orders["ship_date"] = orders["ship_date"].dt.strftime(
            "%Y-%m-%d"
        )

        orders.to_sql(
            "orders",
            connection,
            if_exists="append",
            index=False,
        )

        # Order items
        order_items = sales_data[
            [
                "Order ID",
                "Product ID",
                "Sales",
                "Sales INR",
                "Quantity",
                "Discount",
                "Profit",
                "Profit INR",
                "Shipping Days",
                "Profit Margin",
                "Order Year",
                "Order Month",
                "Order Month Name",
            ]
        ].copy()

        order_items = order_items.rename(
            columns={
                "Order ID": "order_id",
                "Product ID": "product_id",
                "Sales": "sales_usd",
                "Sales INR": "sales_inr",
                "Quantity": "quantity",
                "Discount": "discount",
                "Profit": "profit_usd",
                "Profit INR": "profit_inr",
                "Shipping Days": "shipping_days",
                "Profit Margin": "profit_margin",
                "Order Year": "order_year",
                "Order Month": "order_month",
                "Order Month Name": "order_month_name",
            }
        )

        order_items.to_sql(
            "order_items",
            connection,
            if_exists="append",
            index=False,
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    from src.extraction.api_extractor import extract_exchange_rate
    from src.extraction.csv_extractor import extract_sales_data
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

    load_normalized_data(transformed_data)

    print("Normalized data loaded successfully.")