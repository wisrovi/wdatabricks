from typing import Any, Dict, List, Optional, Tuple, Union
from ..exceptions import QueryError, ValidationError, TransactionError
from .connection import ConnectionManager
from ..types.sql_types import get_sql_type


class WDatabricks:
    def __init__(self, connection_manager: Optional[ConnectionManager] = None):
        self._cm = connection_manager or ConnectionManager.get_instance()

    @property
    def connection_manager(self) -> ConnectionManager:
        return self._cm

    def execute(self, query: str, params: Optional[Tuple] = None) -> Any:
        cursor = self._cm.get_cursor()
        try:
            cursor.execute(query, params or ())
            if query.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
            self._cm.commit()
            return cursor.rowcount
        except Exception as e:
            self._cm.rollback()
            raise QueryError(f"Query execution failed: {e}")
        finally:
            cursor.close()

    def execute_many(self, query: str, params_list: List[Tuple]) -> int:
        cursor = self._cm.get_cursor()
        try:
            cursor.executemany(query, params_list)
            self._cm.commit()
            return cursor.rowcount
        except Exception as e:
            self._cm.rollback()
            raise QueryError(f"Batch execution failed: {e}")
        finally:
            cursor.close()

    def fetch_one(
        self,
        table: str,
        conditions: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        **kwargs,
    ) -> Optional[Dict[str, Any]]:
        query = f"SELECT * FROM {table}"
        params = ()
        if conditions:
            where_clause = " AND ".join([f"{k} = %s" for k in conditions.keys()])
            query += f" WHERE {where_clause}"
            params = tuple(conditions.values())
        if order_by:
            query += f" ORDER BY {order_by}"
        query += " LIMIT 1"
        cursor = self._cm.get_cursor()
        try:
            cursor.execute(query, params)
            row = cursor.fetchone()
            if row is None:
                return None
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))
        finally:
            cursor.close()

    def fetch_all(
        self,
        table: str,
        conditions: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        query = f"SELECT * FROM {table}"
        params = ()
        if conditions:
            where_clause = " AND ".join([f"{k} = %s" for k in conditions.keys()])
            query += f" WHERE {where_clause}"
            params = tuple(conditions.values())
        if order_by:
            query += f" ORDER BY {order_by}"
        if limit:
            query += f" LIMIT {limit}"
        if offset:
            query += f" OFFSET {offset}"
        cursor = self._cm.get_cursor()
        try:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            if not rows:
                return []
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        finally:
            cursor.close()

    def insert(self, table: str, data: Dict[str, Any]) -> int:
        if not data:
            raise ValidationError("Data cannot be empty")
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        return self.execute(query, tuple(data.values()))

    def insert_many(self, table: str, data_list: List[Dict[str, Any]]) -> int:
        if not data_list:
            raise ValidationError("Data list cannot be empty")
        columns = ", ".join(data_list[0].keys())
        placeholders = ", ".join(["%s"] * len(data_list[0]))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        params_list = [tuple(row.values()) for row in data_list]
        return self.execute_many(query, params_list)

    def update(
        self, table: str, data: Dict[str, Any], conditions: Dict[str, Any]
    ) -> int:
        if not data:
            raise ValidationError("Data cannot be empty")
        if not conditions:
            raise ValidationError("Conditions cannot be empty")
        set_clause = ", ".join([f"{k} = %s" for k in data.keys()])
        where_clause = " AND ".join([f"{k} = %s" for k in conditions.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        params = tuple(data.values()) + tuple(conditions.values())
        return self.execute(query, params)

    def delete(self, table: str, conditions: Dict[str, Any]) -> int:
        if not conditions:
            raise ValidationError("Conditions cannot be empty")
        where_clause = " AND ".join([f"{k} = %s" for k in conditions.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"
        return self.execute(query, tuple(conditions.values()))

    def upsert(
        self,
        table: str,
        data: Dict[str, Any],
        key_columns: List[str],
    ) -> int:
        if not data:
            raise ValidationError("Data cannot be empty")
        if not key_columns:
            raise ValidationError("Key columns cannot be empty")

        columns = list(data.keys())
        set_clause = ", ".join(
            [
                f"{k} = {v}" if k in key_columns else f"{k} = {v}"
                for k, v in zip(columns, ["s." + c for c in columns])
            ]
        )
        set_clause = ", ".join([f"{c} = s.{c}" for c in columns])
        where_clause = " AND ".join([f"t.{k} = s.{k}" for k in key_columns])

        query = f"""
        MERGE INTO {table} t
        USING (SELECT {", ".join(["%s as " + c for c in columns])}) s
        ON {where_clause}
        WHEN MATCHED THEN UPDATE SET {set_clause}
        WHEN NOT MATCHED THEN INSERT ({", ".join(columns)}) VALUES ({", ".join(["s." + c for c in columns])})
        """
        params = tuple(data.values())
        return self.execute(query, params)

    def paginate(
        self,
        table: str,
        page: int = 1,
        page_size: int = 20,
        conditions: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
    ) -> Dict[str, Any]:
        if page < 1:
            raise ValidationError("Page must be >= 1")
        if page_size < 1:
            raise ValidationError("Page size must be >= 1")

        where_clause = ""
        params = ()
        if conditions:
            where_clause = " WHERE " + " AND ".join(
                [f"{k} = %s" for k in conditions.keys()]
            )
            params = tuple(conditions.values())

        order_clause = f" ORDER BY {order_by}" if order_by else ""
        offset = (page - 1) * page_size

        count_query = f"SELECT COUNT(*) as total FROM {table}{where_clause}"
        cursor = self._cm.get_cursor()
        try:
            cursor.execute(count_query, params)
            total = cursor.fetchone()[0]
        finally:
            cursor.close()

        data_query = (
            f"SELECT * FROM {table}{where_clause}{order_clause} LIMIT %s OFFSET %s"
        )
        try:
            cursor.execute(data_query, params + (page_size, offset))
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            items = [dict(zip(columns, row)) for row in rows]
        finally:
            cursor.close()

        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size,
        }

    def bulk_insert(
        self, table: str, data_list: List[Dict[str, Any]], batch_size: int = 1000
    ) -> int:
        if not data_list:
            raise ValidationError("Data list cannot be empty")

        total_rows = 0
        for i in range(0, len(data_list), batch_size):
            batch = data_list[i : i + batch_size]
            total_rows += self.insert_many(table, batch)
        return total_rows

    def bulk_update(
        self, table: str, data_list: List[Dict[str, Any]], key_columns: List[str]
    ) -> int:
        total = 0
        for data in data_list:
            key_values = {k: data[k] for k in key_columns}
            non_key = {k: v for k, v in data.items() if k not in key_columns}
            if non_key:
                total += self.update(table, non_key, key_values)
        return total

    def bulk_delete(self, table: str, key_column: str, key_values: List[Any]) -> int:
        total = 0
        for value in key_values:
            total += self.delete(table, {key_column: value})
        return total

    def transaction(self):
        return TransactionContext(self._cm)

    def table_exists(self, table: str) -> bool:
        cursor = self._cm.get_cursor()
        try:
            cursor.execute(f"DESCRIBE TABLE {table}")
            return True
        except Exception:
            return False
        finally:
            cursor.close()

    def list_tables(
        self, catalog: Optional[str] = None, schema: Optional[str] = None
    ) -> List[str]:
        query = "SHOW TABLES"
        if catalog and schema:
            query += f" IN {catalog}.{schema}"
        elif schema:
            query += f" IN {schema}"
        cursor = self._cm.get_cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        finally:
            cursor.close()


class TransactionContext:
    def __init__(self, connection_manager: ConnectionManager):
        self._cm = connection_manager
        self._committed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self._cm.rollback()
            raise TransactionError(f"Transaction failed: {exc_val}")
        if not self._committed:
            self._cm.commit()
        return False

    def commit(self) -> None:
        self._cm.commit()
        self._committed = True

    def rollback(self) -> None:
        self._cm.rollback()
        self._committed = True
