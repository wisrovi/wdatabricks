from typing import Dict, Any, Optional, List
from datetime import datetime, date, time
from decimal import Decimal


class SQLType:
    STRING = "STRING"
    INTEGER = "INTEGER"
    BIGINT = "BIGINT"
    DOUBLE = "DOUBLE"
    DECIMAL = "DECIMAL"
    BOOLEAN = "BOOLEAN"
    TIMESTAMP = "TIMESTAMP"
    DATE = "DATE"
    ARRAY = "ARRAY"
    MAP = "MAP"
    STRUCT = "STRUCT"
    BINARY = "BINARY"
    FLOAT = "FLOAT"


PYTHON_TO_SQL: Dict[type, str] = {
    str: SQLType.STRING,
    int: SQLType.INTEGER,
    float: SQLType.DOUBLE,
    bool: SQLType.BOOLEAN,
    bytes: SQLType.BINARY,
    bytearray: SQLType.BINARY,
    datetime: SQLType.TIMESTAMP,
    date: SQLType.DATE,
    time: SQLType.STRING,
    Decimal: SQLType.DECIMAL,
    list: SQLType.ARRAY,
    dict: SQLType.MAP,
    type(None): SQLType.STRING,
}


SQL_TO_PYTHON: Dict[str, type] = {
    SQLType.STRING: str,
    SQLType.INTEGER: int,
    SQLType.BIGINT: int,
    SQLType.DOUBLE: float,
    SQLType.DECIMAL: Decimal,
    SQLType.BOOLEAN: bool,
    SQLType.TIMESTAMP: datetime,
    SQLType.DATE: date,
    SQLType.ARRAY: list,
    SQLType.MAP: dict,
    SQLType.STRUCT: dict,
    SQLType.BINARY: bytes,
    SQLType.FLOAT: float,
}


def get_sql_type(python_type: type) -> str:
    if python_type in PYTHON_TO_SQL:
        return PYTHON_TO_SQL[python_type]
    if python_type == float:
        return SQLType.FLOAT
    if python_type == list:
        return SQLType.ARRAY
    if python_type == dict:
        return SQLType.MAP
    return SQLType.STRING


def get_python_type(sql_type: str) -> type:
    return SQL_TO_PYTHON.get(sql_type, str)


class ColumnDefinition:
    def __init__(
        self,
        name: str,
        sql_type: str,
        nullable: bool = True,
        default: Optional[Any] = None,
        comment: Optional[str] = None,
    ):
        self.name = name
        self.sql_type = sql_type
        self.nullable = nullable
        self.default = default
        self.comment = comment

    def to_sql(self) -> str:
        parts = [f"{self.name} {self.sql_type}"]
        if not self.nullable:
            parts.append("NOT NULL")
        if self.default is not None:
            parts.append(f"DEFAULT {self._format_default()}")
        if self.comment:
            parts.append(f"COMMENT '{self.comment}'")
        return " ".join(parts)

    def _format_default(self) -> str:
        if isinstance(self.default, str):
            return f"'{self.default}'"
        if isinstance(self.default, (list, dict)):
            import json

            return f"'{json.dumps(self.default)}'"
        return str(self.default)

    def __repr__(self) -> str:
        return (
            f"ColumnDefinition({self.name}, {self.sql_type}, nullable={self.nullable})"
        )


class TableDefinition:
    def __init__(
        self,
        name: str,
        columns: List[ColumnDefinition],
        comment: Optional[str] = None,
        partition_by: Optional[List[str]] = None,
    ):
        self.name = name
        self.columns = columns
        self.comment = comment
        self.partition_by = partition_by

    def to_sql(self) -> str:
        col_sql = ", ".join(col.to_sql() for col in self.columns)
        parts = [f"CREATE TABLE IF NOT EXISTS {self.name} ({col_sql})"]
        if self.comment:
            parts.append(f"COMMENT '{self.comment}'")
        if self.partition_by:
            parts.append(f"PARTITIONED BY ({', '.join(self.partition_by)})")
        return " ".join(parts)

    def __repr__(self) -> str:
        return f"TableDefinition({self.name}, {len(self.columns)} columns)"
