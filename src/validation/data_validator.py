import pandas as pd


def validate_sales_data(sales_data: pd.DataFrame) -> dict:
    """
    Run basic data-quality checks on the transformed sales data.

    Args:
        sales_data: Transformed sales DataFrame.

    Returns:
        dict: Validation results.
    """
    required_columns = [
        "Order ID",
        "Customer ID",
        "Product ID",
        "Order Date",
        "Ship Date",
        "Sales",
        "Quantity",
        "Discount",
        "Profit",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in sales_data.columns
    ]

    results = {
        "row_count": len(sales_data),
        "missing_required_columns": missing_columns,
        "missing_values": int(
            sales_data[required_columns].isnull().sum().sum()
        ) if not missing_columns else None,
        "duplicate_rows": int(sales_data.duplicated().sum()),
        "invalid_sales": int((sales_data["Sales"] < 0).sum()),
        "invalid_quantity": int((sales_data["Quantity"] <= 0).sum()),
        "invalid_discount": int(
            ((sales_data["Discount"] < 0) | (sales_data["Discount"] > 1)).sum()
        ),
        "invalid_dates": int(
            (
                sales_data["Order Date"].isnull()
                | sales_data["Ship Date"].isnull()
            ).sum()
        ),
    }

    results["is_valid"] = (
        len(results["missing_required_columns"]) == 0
        and results["missing_values"] == 0
        and results["duplicate_rows"] == 0
        and results["invalid_sales"] == 0
        and results["invalid_quantity"] == 0
        and results["invalid_discount"] == 0
        and results["invalid_dates"] == 0
    )

    return results


if __name__ == "__main__":
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

    validation_results = validate_sales_data(transformed_data)

    print("Data Quality Results")
    print("--------------------")

    for check, result in validation_results.items():
        print(f"{check}: {result}")