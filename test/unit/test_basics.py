import pytest


class TestWDatabricksImport:
    def test_import(self):
        from wdatabricks import WDatabricks

        assert WDatabricks is not None

    def test_version(self):
        import wdatabricks

        assert wdatabricks.__version__ == "1.0.0"


class TestQueryBuilder:
    def test_import(self):
        from wdatabricks import QueryBuilder

        qb = QueryBuilder()
        assert qb is not None


class TestExceptions:
    def test_import(self):
        from wdatabricks import WDatabricksError

        with pytest.raises(WDatabricksError):
            raise WDatabricksError("test")
