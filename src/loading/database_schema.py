import sqlite3

from config.config import DATABASE_FILE


def create_database_schema() -> None:
    """
    Create the normalized SQLite database schema.
    """
    DATABASE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(DATABASE_FILE)

    try:
        cursor = connection.cursor()

        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.executescript(
            """
            DROP TABLE IF EXISTS order_items;
            DROP TABLE IF EXISTS orders;
            DROP TABLE IF EXISTS products;
            DROP TABLE IF EXISTS customers;
            DROP TABLE IF EXISTS sales;
            CREATE TABLE customers (
                customer_id TEXT PRIMARY KEY,
                customer_name TEXT NOT NULL,
                segment TEXT
            );

            CREATE TABLE products (
                product_id TEXT PRIMARY KEY,
                product_name TEXT NOT NULL,
                category TEXT,
                sub_category TEXT
            );

            CREATE TABLE orders (
                order_id TEXT PRIMARY KEY,
                order_date TEXT NOT NULL,
                ship_date TEXT NOT NULL,
                ship_mode TEXT,
                customer_id TEXT NOT NULL,
                country TEXT,
                city TEXT,
                state TEXT,
                postal_code TEXT,
                region TEXT,
                FOREIGN KEY (customer_id)
                    REFERENCES customers(customer_id)
            );

            CREATE TABLE order_items (
                 order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 order_id TEXT NOT NULL,
                 product_id TEXT NOT NULL,
                 sales_usd REAL NOT NULL,
                 sales_inr REAL NOT NULL,
                 quantity INTEGER NOT NULL,
                 discount REAL NOT NULL,
                 profit_usd REAL NOT NULL,
                 profit_inr REAL NOT NULL,
                 shipping_days INTEGER,
                 profit_margin REAL,
                 order_year INTEGER,
                 order_month INTEGER,
                 order_month_name TEXT,
                 FOREIGN KEY (order_id)
                     REFERENCES orders(order_id),
                 FOREIGN KEY (product_id)
                     REFERENCES products(product_id)
            );
            """
        )

        connection.commit()

    finally:
        connection.close()


if __name__ == "__main__":
    create_database_schema()

    print(f"Database schema created: {DATABASE_FILE}")