from typing import Any, Dict, List, Optional, Tuple


class QueryBuilder:
    def __init__(self):
        self._select_parts: List[str] = []
        self._from_table: Optional[str] = None
        self._joins: List[str] = []
        self._where_parts: List[str] = []
        self._group_by: List[str] = []
        self._having_parts: List[str] = []
        self._order_by: List[str] = []
        self._limit_value: Optional[int] = None
        self._offset_value: Optional[int] = None
        self._params: List[Any] = []

    def select(self, *columns: str) -> "QueryBuilder":
        if not columns:
            self._select_parts = ["*"]
        else:
            self._select_parts = list(columns)
        return self

    def select_distinct(self, *columns: str) -> "QueryBuilder":
        if not columns:
            self._select_parts = ["DISTINCT *"]
        else:
            self._select_parts = [f"DISTINCT {', '.join(columns)}"]
        return self

    def from_table(self, table: str) -> "QueryBuilder":
        self._from_table = table
        return self

    def join(
        self,
        table: str,
        condition: str,
        join_type: str = "INNER",
    ) -> "QueryBuilder":
        self._joins.append(f"{join_type} JOIN {table} ON {condition}")
        return self

    def left_join(self, table: str, condition: str) -> "QueryBuilder":
        return self.join(table, condition, "LEFT")

    def right_join(self, table: str, condition: str) -> "QueryBuilder":
        return self.join(table, condition, "RIGHT")

    def inner_join(self, table: str, condition: str) -> "QueryBuilder":
        return self.join(table, condition, "INNER")

    def where(self, condition: str, *params: Any) -> "QueryBuilder":
        self._where_parts.append(f"({condition})")
        self._params.extend(params)
        return self

    def where_in(self, column: str, values: List[Any]) -> "QueryBuilder":
        placeholders = ", ".join(["%s"] * len(values))
        self._where_parts.append(f"{column} IN ({placeholders})")
        self._params.extend(values)
        return self

    def where_not_in(self, column: str, values: List[Any]) -> "QueryBuilder":
        placeholders = ", ".join(["%s"] * len(values))
        self._where_parts.append(f"{column} NOT IN ({placeholders})")
        self._params.extend(values)
        return self

    def where_is_null(self, column: str) -> "QueryBuilder":
        self._where_parts.append(f"{column} IS NULL")
        return self

    def where_is_not_null(self, column: str) -> "QueryBuilder":
        self._where_parts.append(f"{column} IS NOT NULL")
        return self

    def where_between(self, column: str, start: Any, end: Any) -> "QueryBuilder":
        self._where_parts.append(f"{column} BETWEEN %s AND %s")
        self._params.extend([start, end])
        return self

    def and_where(self, condition: str, *params: Any) -> "QueryBuilder":
        if self._where_parts:
            self._where_parts.append(f"AND ({condition})")
        else:
            return self.where(condition, *params)
        self._params.extend(params)
        return self

    def or_where(self, condition: str, *params: Any) -> "QueryBuilder":
        if self._where_parts:
            self._where_parts.append(f"OR ({condition})")
        else:
            return self.where(condition, *params)
        self._params.extend(params)
        return self

    def group_by(self, *columns: str) -> "QueryBuilder":
        self._group_by.extend(columns)
        return self

    def having(self, condition: str, *params: Any) -> "QueryBuilder":
        self._having_parts.append(f"({condition})")
        self._params.extend(params)
        return self

    def order_by(self, column: str, direction: str = "ASC") -> "QueryBuilder":
        direction = direction.upper()
        if direction not in ("ASC", "DESC"):
            direction = "ASC"
        self._order_by.append(f"{column} {direction}")
        return self

    def limit(self, limit: int) -> "QueryBuilder":
        self._limit_value = limit
        return self

    def offset(self, offset: int) -> "QueryBuilder":
        self._offset_value = offset
        return self

    def page(self, page: int, page_size: int = 20) -> "QueryBuilder":
        self._limit_value = page_size
        self._offset_value = (page - 1) * page_size
        return self

    def build(self) -> Tuple[str, Tuple[Any, ...]]:
        if not self._from_table:
            raise ValueError("Table not specified. Call from_table() first.")

        parts = ["SELECT"]

        if self._select_parts:
            parts.append(", ".join(self._select_parts))
        else:
            parts.append("*")

        parts.append(f"FROM {self._from_table}")

        if self._joins:
            parts.append(" ".join(self._joins))

        if self._where_parts:
            parts.append("WHERE " + " ".join(self._where_parts))

        if self._group_by:
            parts.append("GROUP BY " + ", ".join(self._group_by))

        if self._having_parts:
            parts.append("HAVING " + " ".join(self._having_parts))

        if self._order_by:
            parts.append("ORDER BY " + ", ".join(self._order_by))

        if self._limit_value is not None:
            parts.append(f"LIMIT {self._limit_value}")

        if self._offset_value is not None:
            parts.append(f"OFFSET {self._offset_value}")

        query = " ".join(parts)
        return query, tuple(self._params)

    def build_count(self) -> Tuple[str, Tuple[Any, ...]]:
        if not self._from_table:
            raise ValueError("Table not specified. Call from_table() first.")

        parts = ["SELECT COUNT(*) as count"]

        parts.append(f"FROM {self._from_table}")

        if self._joins:
            parts.append(" ".join(self._joins))

        if self._where_parts:
            parts.append("WHERE " + " ".join(self._where_parts))

        if self._group_by:
            parts.append("GROUP BY " + ", ".join(self._group_by))

        if self._having_parts:
            parts.append("HAVING " + " ".join(self._having_parts))

        query = " ".join(parts)
        return query, tuple(self._params)

    def to_sql(self) -> str:
        query, _ = self.build()
        return query

    def get_params(self) -> Tuple[Any, ...]:
        _, params = self.build()
        return params

    def reset(self) -> "QueryBuilder":
        self.__init__()
        return self
