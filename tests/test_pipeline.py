import sqlite3

from config.config import DATABASE_FILE
from src.pipeline import run_pipeline


def test_pipeline() -> None:
    """Verify that the complete ETL pipeline runs successfully."""
    run_pipeline()

    connection = sqlite3.connect(DATABASE_FILE)

    try:
        cursor = connection.cursor()

        expected_tables = {
            "customers",
            "products",
            "orders",
            "order_items",
        }

        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """
        )

        actual_tables = {
            row[0]
            for row in cursor.fetchall()
        }

        assert expected_tables.issubset(actual_tables)

        cursor.execute("SELECT COUNT(*) FROM order_items")

        order_item_count = cursor.fetchone()[0]

        assert order_item_count == 10194

    finally:
        connection.close()


if __name__ == "__main__":
    test_pipeline()
    print("End-to-end pipeline test passed.")