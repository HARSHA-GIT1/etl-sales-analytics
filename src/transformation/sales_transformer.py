import pandas as pd


def transform_sales_data(
    sales_data: pd.DataFrame,
    exchange_rate: float,
) -> pd.DataFrame:
    """
    Apply analytics-oriented transformations to the raw sales data.

    Args:
        sales_data: Raw sales DataFrame.
        exchange_rate: USD to INR exchange rate.

    Returns:
        pd.DataFrame: Transformed sales data.
    """
    transformed_data = sales_data.copy()

    # Convert date columns to datetime.
    transformed_data["Order Date"] = pd.to_datetime(
        transformed_data["Order Date"],
        errors="coerce",
    )

    transformed_data["Ship Date"] = pd.to_datetime(
        transformed_data["Ship Date"],
        errors="coerce",
    )

    # Convert USD-based financial values to INR.
    transformed_data["Sales INR"] = (
        transformed_data["Sales"] * exchange_rate
    )

    transformed_data["Profit INR"] = (
        transformed_data["Profit"] * exchange_rate
    )

    # Calculate shipping duration.
    transformed_data["Shipping Days"] = (
        transformed_data["Ship Date"]
        - transformed_data["Order Date"]
    ).dt.days

    # Calculate profit margin.
    transformed_data["Profit Margin"] = (
        transformed_data["Profit"] / transformed_data["Sales"]
    ).where(
        transformed_data["Sales"] != 0
    )

    # Create date-based analytics fields.
    transformed_data["Order Year"] = (
        transformed_data["Order Date"].dt.year
    )

    transformed_data["Order Month"] = (
        transformed_data["Order Date"].dt.month
    )

    transformed_data["Order Month Name"] = (
        transformed_data["Order Date"].dt.strftime("%B")
    )

    return transformed_data