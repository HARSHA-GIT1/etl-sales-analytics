import sqlite3

from config.config import DATABASE_FILE


def create_analytics_view() -> None:
    """
    Create a denormalized analytics view for Power BI.
    """
    connection = sqlite3.connect(DATABASE_FILE)

    try:
        connection.execute("PRAGMA foreign_keys = ON")

        connection.execute("DROP VIEW IF EXISTS sales_analytics")

        connection.execute(
            """
            CREATE VIEW sales_analytics AS
            SELECT
                oi.order_item_id,
                oi.order_id,
                oi.product_id,

                o.order_date,
                o.ship_date,
                o.ship_mode,
                o.country,
                o.city,
                o.state,
                o.postal_code,
                o.region,

                c.customer_id,
                c.customer_name,
                c.segment,

                p.product_name,
                p.category,
                p.sub_category,

                oi.sales_usd,
                oi.sales_inr,
                oi.quantity,
                oi.discount,
                oi.profit_usd,
                oi.profit_inr,

                oi.shipping_days,
                oi.profit_margin,
                oi.order_year,
                oi.order_month,
                oi.order_month_name

            FROM order_items oi

            INNER JOIN orders o
                ON oi.order_id = o.order_id

            INNER JOIN customers c
                ON o.customer_id = c.customer_id

            INNER JOIN products p
                ON oi.product_id = p.product_id
            """
        )

        connection.commit()

    finally:
        connection.close()


if __name__ == "__main__":
    create_analytics_view()

    print("Power BI analytics view created successfully.")