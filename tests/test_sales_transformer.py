import pandas as pd

from src.extraction.csv_extractor import extract_sales_data
from src.extraction.api_extractor import extract_exchange_rate
from src.transformation.sales_transformer import transform_sales_data


sales_data = extract_sales_data()

exchange_data = extract_exchange_rate()

exchange_rate = exchange_data["rates"]["INR"]

transformed_data = transform_sales_data(
    sales_data,
    exchange_rate,
)

print("Rows:", len(transformed_data))
print("Order Date type:", transformed_data["Order Date"].dtype)
print("Ship Date type:", transformed_data["Ship Date"].dtype)
print("New columns:")
print(
    transformed_data[
        ["Sales", "Sales INR", "Profit", "Profit INR"]
    ].head()
)