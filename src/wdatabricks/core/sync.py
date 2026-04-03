from typing import Dict, List, Optional, Any
from .connection import ConnectionManager
from ..exceptions import SchemaError, QueryError
from ..types.sql_types import ColumnDefinition, TableDefinition, get_sql_type


class TableSync:
    def __init__(self, connection_manager: Optional[ConnectionManager] = None):
        self._cm = connection_manager or ConnectionManager.get_instance()

    def create_table(
        self,
        table_name: str,
        columns: List[ColumnDefinition],
        comment: Optional[str] = None,
        partition_by: Optional[List[str]] = None,
    ) -> bool:
        cursor = self._cm.get_cursor()
        try:
            table_def = TableDefinition(
                name=table_name,
                columns=columns,
                comment=comment,
                partition_by=partition_by,
            )
            cursor.execute(table_def.to_sql())
            self._cm.commit()
            return True
        except Exception as e:
            self._cm.rollback()
            raise SchemaError(f"Failed to create table {table_name}: {e}")
        finally:
            cursor.close()

    def create_table_if_not_exists(
        self,
        table_name: str,
        columns: List[ColumnDefinition],
        comment: Optional[str] = None,
        partition_by: Optional[List[str]] = None,
    ) -> bool:
        if self.table_exists(table_name):
            return False
        return self.create_table(table_name, columns, comment, partition_by)

    def drop_table(self, table_name: str, if_exists: bool = True) -> bool:
        cursor = self._cm.get_cursor()
        try:
            if if_exists:
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            else:
                cursor.execute(f"DROP TABLE {table_name}")
            self._cm.commit()
            return True
        except Exception as e:
            self._cm.rollback()
            raise SchemaError(f"Failed to drop table {table_name}: {e}")
        finally:
            cursor.close()

    def add_column(
        self,
        table_name: str,
        column: ColumnDefinition,
    ) -> bool:
        if not self.table_exists(table_name):
            raise SchemaError(f"Table {table_name} does not exist")

        cursor = self._cm.get_cursor()
        try:
            query = f"ALTER TABLE {table_name} ADD COLUMNS ({column.to_sql()})"
            cursor.execute(query)
            self._cm.commit()
            return True
        except Exception as e:
            self._cm.rollback()
            raise SchemaError(f"Failed to add column {column.name}: {e}")
        finally:
            cursor.close()

    def alter_column(
        self,
        table_name: str,
        column_name: str,
        new_type: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> bool:
        cursor = self._cm.get_cursor()
        try:
            changes = []
            if new_type:
                changes.append(f"ALTER COLUMN {column_name} TYPE {new_type}")
            if comment is not None:
                changes.append(f"ALTER COLUMN {column_name} COMMENT '{comment}'")

            for change in changes:
                query = f"ALTER TABLE {table_name} {change}"
                cursor.execute(query)
            self._cm.commit()
            return True
        except Exception as e:
            self._cm.rollback()
            raise SchemaError(f"Failed to alter column {column_name}: {e}")
        finally:
            cursor.close()

    def drop_column(self, table_name: str, column_name: str) -> bool:
        cursor = self._cm.get_cursor()
        try:
            query = f"ALTER TABLE {table_name} DROP COLUMN {column_name}"
            cursor.execute(query)
            self._cm.commit()
            return True
        except Exception as e:
            self._cm.rollback()
            raise SchemaError(f"Failed to drop column {column_name}: {e}")
        finally:
            cursor.close()

    def table_exists(self, table_name: str) -> bool:
        cursor = self._cm.get_cursor()
        try:
            cursor.execute(f"DESCRIBE TABLE {table_name}")
            return True
        except Exception:
            return False
        finally:
            cursor.close()

    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        cursor = self._cm.get_cursor()
        try:
            cursor.execute(f"DESCRIBE TABLE {table_name}")
            rows = cursor.fetchall()
            schema = []
            for row in rows:
                schema.append(
                    {
                        "name": row[0],
                        "type": row[1],
                        "comment": row[2] if len(row) > 2 else None,
                    }
                )
            return schema
        finally:
            cursor.close()

    def get_column_info(
        self, table_name: str, column_name: str
    ) -> Optional[Dict[str, Any]]:
        schema = self.get_table_schema(table_name)
        for col in schema:
            if col["name"] == column_name:
                return col
        return None

    def column_exists(self, table_name: str, column_name: str) -> bool:
        return self.get_column_info(table_name, column_name) is not None

    def sync_columns(
        self,
        table_name: str,
        columns: List[ColumnDefinition],
    ) -> Dict[str, Any]:
        if not self.table_exists(table_name):
            raise SchemaError(f"Table {table_name} does not exist")

        result = {"added": [], "skipped": 0, "errors": []}
        existing_columns = {
            col["name"]: col for col in self.get_table_schema(table_name)
        }

        for column in columns:
            if column.name in existing_columns:
                result["skipped"] += 1
                continue
            try:
                self.add_column(table_name, column)
                result["added"].append(column.name)
            except Exception as e:
                result["errors"].append({"column": column.name, "error": str(e)})

        return result

    def truncate_table(self, table_name: str) -> bool:
        cursor = self._cm.get_cursor()
        try:
            cursor.execute(f"TRUNCATE TABLE {table_name}")
            self._cm.commit()
            return True
        except Exception as e:
            self._cm.rollback()
            raise SchemaError(f"Failed to truncate table {table_name}: {e}")
        finally:
            cursor.close()
