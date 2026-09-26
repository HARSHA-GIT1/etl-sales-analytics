from pathlib import Path
import sqlite3

from config.config import DATABASE_FILE


def check_project() -> None:
    """Check that the main project files and database exist."""

    required_files = [
        Path("data/raw/samplesuperstore.csv"),
        Path("data/processed/sales.db"),
        Path("src/pipeline.py"),
        Path("src/extraction/csv_extractor.py"),
        Path("src/extraction/api_extractor.py"),
        Path("src/transformation/sales_transformer.py"),
        Path("src/validation/data_validator.py"),
        Path("src/loading/database_schema.py"),
        Path("src/loading/normalized_loader.py"),
        Path("src/logging_config.py"),
    ]

    print("PROJECT FILE CHECK")
    print("------------------")

    for file_path in required_files:
        status = "OK" if file_path.exists() else "MISSING"
        print(f"{file_path}: {status}")

    print("\nDATABASE CHECK")
    print("--------------")

    connection = sqlite3.connect(DATABASE_FILE)

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name
            """
        )

        tables = [row[0] for row in cursor.fetchall()]

        print("Tables:", tables)

    finally:
        connection.close()


if __name__ == "__main__":
    check_project()