from src.extraction.api_extractor import extract_exchange_rate
from src.extraction.csv_extractor import extract_sales_data
from src.loading.analytics_view import create_analytics_view
from src.loading.database_schema import create_database_schema
from src.loading.normalized_loader import load_normalized_data
from src.logging_config import get_logger
from src.transformation.sales_transformer import transform_sales_data
from src.validation.data_validator import validate_sales_data


logger = get_logger()


def run_pipeline() -> None:
    """
    Run the complete ETL pipeline.

    Flow:
        Extract -> Transform -> Validate -> Load -> Create Analytics View
    """
    logger.info("ETL pipeline started.")

    try:
        logger.info("Extracting sales data.")
        sales_data = extract_sales_data()

        logger.info("Extracting exchange rate.")
        exchange_data = extract_exchange_rate()
        exchange_rate = exchange_data["rates"]["INR"]

        logger.info(
            "USD to INR exchange rate: %s",
            exchange_rate,
        )

        logger.info("Transforming sales data.")
        transformed_data = transform_sales_data(
            sales_data,
            exchange_rate,
        )

        logger.info("Validating sales data.")
        validation_results = validate_sales_data(
            transformed_data
        )

        if not validation_results["is_valid"]:
            logger.error(
                "Data validation failed: %s",
                validation_results,
            )
            raise ValueError("Data validation failed.")

        logger.info("Data validation passed.")

        logger.info("Creating database schema.")
        create_database_schema()

        logger.info("Loading data into SQLite.")
        load_normalized_data(transformed_data)

        logger.info("Creating analytics view.")
        create_analytics_view()

        logger.info("ETL pipeline completed successfully.")

    except Exception:
        logger.exception("ETL pipeline failed.")
        raise


if __name__ == "__main__":
    run_pipeline()