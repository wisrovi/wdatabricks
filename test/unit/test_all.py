"""
Comprehensive test suite for wdatabricks library.
"""

import pytest


class TestWDatabricksImport:
    """Test basic imports."""

    def test_import_main_class(self):
        from wdatabricks import WDatabricks

        assert WDatabricks is not None

    def test_import_connection_manager(self):
        from wdatabricks import ConnectionManager

        assert ConnectionManager is not None

    def test_import_query_builder(self):
        from wdatabricks import QueryBuilder

        assert QueryBuilder is not None

    def test_version(self):
        import wdatabricks

        assert wdatabricks.__version__ == "1.0.0"


class TestExceptions:
    """Test exception hierarchy."""

    def test_wdatabricks_error(self):
        from wdatabricks import WDatabricksError

        with pytest.raises(WDatabricksError):
            raise WDatabricksError("test")

    def test_connection_error(self):
        from wdatabricks import ConnectionError

        with pytest.raises(ConnectionError):
            raise ConnectionError("test")

    def test_query_error(self):
        from wdatabricks import QueryError

        with pytest.raises(QueryError):
            raise QueryError("test")

    def test_hierarchy(self):
        from wdatabricks import WDatabricksError, ConnectionError

        assert issubclass(ConnectionError, WDatabricksError)


class TestQueryBuilder:
    """Test QueryBuilder."""

    def test_fluent_api(self):
        from wdatabricks import QueryBuilder

        qb = QueryBuilder().select("*").from_table("users")
        assert qb is not None

    def test_where(self):
        from wdatabricks import QueryBuilder

        qb = QueryBuilder().select("*").from_table("users").where("id", "=", 1)
        query, _ = qb.build_select()
        assert "WHERE" in query

    def test_order_by(self):
        from wdatabricks import QueryBuilder

        qb = QueryBuilder().select("*").from_table("users").order_by("name")
        query, _ = qb.build_select()
        assert "ORDER BY name" in query


class TestConnectionManager:
    """Test ConnectionManager."""

    def test_init(self):
        from wdatabricks import ConnectionManager

        cm = ConnectionManager(
            server_hostname="test.cloud.databricks.com",
            http_path="/sql/1.0/warehouses/test",
            access_token="test_token",
        )
        assert cm is not None

    def test_singleton(self):
        from wdatabricks import ConnectionManager

        cm1 = ConnectionManager(
            server_hostname="test.cloud.databricks.com",
            http_path="/sql/1.0/warehouses/test",
            access_token="test_token",
        )
        cm2 = ConnectionManager(
            server_hostname="test.cloud.databricks.com",
            http_path="/sql/1.0/warehouses/test",
            access_token="test_token",
        )
        assert cm1 is cm2


class TestSqlTypes:
    """Test SQL type mapping."""

    def test_varchar_type(self):
        from wdatabricks.types import get_sql_type
        from pydantic import BaseModel

        class TestModel(BaseModel):
            name: str

        sql_type = get_sql_type(TestModel.model_fields["name"])
        assert "STRING" in sql_type

    def test_integer_type(self):
        from wdatabricks.types import get_sql_type
        from pydantic import BaseModel

        class TestModel(BaseModel):
            id: int

        sql_type = get_sql_type(TestModel.model_fields["id"])
        assert "INT" in sql_type
