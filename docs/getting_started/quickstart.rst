Quickstart
===========

This guide will help you get started with wdatabricks quickly.

Basic Usage
-----------

.. code-block:: python

    from wdatabricks import WDatabricks, ConnectionManager

    cm = ConnectionManager(
        server_hostname="your-server.cloud.databricks.com",
        http_path="/sql/your-warehouse",
        access_token="your-access-token"
    )

    db = WDatabricks(cm)

    result = db.fetch_all("SELECT * FROM my_table")
    print(result)

Execute Queries
---------------

.. code-block:: python

    db.execute("CREATE TABLE IF NOT EXISTS users (id INT, name STRING)")

    db.execute("INSERT INTO users VALUES (1, 'John')")

    result = db.fetch_all("SELECT * FROM users")

Using QueryBuilder
-----------------

.. code-block:: python

    from wdatabricks import QueryBuilder

    query = (QueryBuilder()
        .select("id", "name", "email")
        .from_table("users")
        .where("active", "=", True)
        .limit(100)
        .build())

    results = db.execute(query)