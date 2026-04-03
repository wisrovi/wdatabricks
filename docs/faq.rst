FAQ
===

Frequently Asked Questions about wdatabricks.

General
-------

What is wdatabricks?
~~~~~~~~~~~~~~~~~~~~

wdatabricks is a Python ORM library for Databricks providing SQL query execution and connection management.

What Python versions are supported?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

wdatabricks supports Python 3.8 and later.

Connection
----------

How do I configure the connection?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wdatabricks import ConnectionManager

    cm = ConnectionManager(
        server_hostname="your-server.cloud.databricks.com",
        http_path="/sql/your-warehouse",
        access_token="your-access-token"
    )

Where do I find the HTTP path?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In Databricks, go to SQL Warehouses -> Your Warehouse -> Connection Details.

Errors
------

What exceptions does wdatabricks raise?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``WDatabricksError`` - Base exception
- ``ConnectionError`` - Connection failures
- ``QueryError`` - Query execution errors
- ``ValidationError`` - Data validation errors