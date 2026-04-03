class WDatabricksError(Exception):
    pass


class ConnectionError(WDatabricksError):
    pass


class QueryError(WDatabricksError):
    pass


class ValidationError(WDatabricksError):
    pass


class TransactionError(WDatabricksError):
    pass


class SchemaError(WDatabricksError):
    pass
