import sqlite3

from config.config import DATABASE_FILE


connection = sqlite3.connect(DATABASE_FILE)

try:
    cursor = connection.cursor()

    print("TABLE COUNTS")
    print("------------")

    tables = [
        "customers",
        "products",
        "orders",
        "order_items",
    ]

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table}: {count}")

    print("\nSAMPLE JOIN")
    print("-----------")

    cursor.execute(
        """
        SELECT
            o.order_id,
            c.customer_name,
            p.product_name,
            oi.sales_inr,
            oi.profit_inr
        FROM order_items oi
        JOIN orders o
            ON oi.order_id = o.order_id
        JOIN customers c
            ON o.customer_id = c.customer_id
        JOIN products p
            ON oi.product_id = p.product_id
        LIMIT 5
        """
    )

    for row in cursor.fetchall():
        print(row)

finally:
    connection.close()