Basic Operations
=================

This tutorial covers basic database operations with wdatabricks.

Setup
-----

.. code-block:: python

    from wdatabricks import WDatabricks, ConnectionManager

    cm = ConnectionManager(
        server_hostname="your-server.cloud.databricks.com",
        http_path="/sql/your-warehouse",
        access_token="your-access-token"
    )

    db = WDatabricks(cm)

Execute Queries
---------------

.. code-block:: python

    db.execute("CREATE TABLE IF NOT EXISTS sales (id INT, amount DOUBLE, date DATE)")

    db.execute("INSERT INTO sales VALUES (1, 100.50, '2024-01-01')")

Fetch Results
-------------

.. code-block:: python

    rows = db.fetch_all("SELECT * FROM sales")
    for row in rows:
        print(row)

    row = db.fetch_one("SELECT * FROM sales WHERE id = 1")

Parameterized Queries
---------------------

.. code-block:: python

    rows = db.fetch_all(
        "SELECT * FROM sales WHERE amount > ?",
        params=(50,)
    )