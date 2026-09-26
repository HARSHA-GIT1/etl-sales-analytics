import sqlite3

from config.config import DATABASE_FILE


connection = sqlite3.connect(DATABASE_FILE)

try:
    cursor = connection.cursor()

    print("1. ANALYTICS COLUMNS")
    print("--------------------")

    cursor.execute("PRAGMA table_info(order_items)")

    columns = cursor.fetchall()

    for column in columns:
        print(column[1])

    print("\n2. TOTAL SALES AND PROFIT")
    print("-------------------------")

    cursor.execute(
        """
        SELECT
            ROUND(SUM(sales_inr), 2) AS total_sales_inr,
            ROUND(SUM(profit_inr), 2) AS total_profit_inr
        FROM order_items
        """
    )

    print(cursor.fetchone())

    print("\n3. SALES BY REGION")
    print("------------------")

    cursor.execute(
        """
        SELECT
            o.region,
            ROUND(SUM(oi.sales_inr), 2) AS sales_inr,
            ROUND(SUM(oi.profit_inr), 2) AS profit_inr
        FROM order_items oi
        JOIN orders o
            ON oi.order_id = o.order_id
        GROUP BY o.region
        ORDER BY sales_inr DESC
        """
    )

    for row in cursor.fetchall():
        print(row)

    print("\n4. TOP 5 PRODUCTS BY SALES")
    print("--------------------------")

    cursor.execute(
        """
        SELECT
            p.product_name,
            ROUND(SUM(oi.sales_inr), 2) AS sales_inr
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        GROUP BY p.product_id, p.product_name
        ORDER BY sales_inr DESC
        LIMIT 5
        """
    )

    for row in cursor.fetchall():
        print(row)

    print("\n5. AVERAGE PROFIT MARGIN")
    print("------------------------")

    cursor.execute(
        """
        SELECT
            ROUND(AVG(profit_margin) * 100, 2) AS average_profit_margin_percent
        FROM order_items
        WHERE profit_margin IS NOT NULL
        """
    )

    print(cursor.fetchone())

finally:
    connection.close()