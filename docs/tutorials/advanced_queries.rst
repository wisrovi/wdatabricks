Advanced Queries
=================

Advanced query patterns with wdatabricks.

QueryBuilder
------------

.. code-block:: python

    from wdatabricks import QueryBuilder

    query = (QueryBuilder()
        .select("s.id", "s.amount", "c.name")
        .from_table("sales", "s")
        .join("customers", "c", "s.customer_id = c.id")
        .where("s.amount", ">", 100)
        .order_by("s.amount", "DESC")
        .limit(50)
        .build())

    results = db.execute(query)

Aggregations
------------

.. code-block:: python

    query = (QueryBuilder()
        .select("COUNT(*)", "SUM(amount)", "AVG(amount)", "MAX(amount)")
        .from_table("sales")
        .build())

    result = db.execute(query)

Subqueries
----------

.. code-block:: python

    query = (QueryBuilder()
        .select("*")
        .from_table("sales")
        .where_in("customer_id",
            QueryBuilder()
            .select("id")
            .from_table("customers")
            .where("tier", "=", "premium")
            .build()
        )
        .build())