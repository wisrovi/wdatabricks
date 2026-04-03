import os
from typing import Optional, Dict, Any
import threading

try:
    from databricks import sql

    DATABRICKS_SQL_AVAILABLE = True
except ImportError:
    DATABRICKS_SQL_AVAILABLE = False

from ..exceptions import ConnectionError as WConnectionError


class ConnectionManager:
    _instance: Optional["ConnectionManager"] = None
    _lock = threading.Lock()

    def __init__(
        self,
        server_hostname: Optional[str] = None,
        http_path: Optional[str] = None,
        access_token: Optional[str] = None,
        catalog: Optional[str] = None,
        schema: Optional[str] = None,
    ):
        self.server_hostname = server_hostname or os.environ.get(
            "DATABRICKS_SERVER_HOSTNAME"
        )
        self.http_path = http_path or os.environ.get("DATABRICKS_HTTP_PATH")
        self.access_token = access_token or os.environ.get("DATABRICKS_ACCESS_TOKEN")
        self.catalog = catalog or os.environ.get("DATABRICKS_CATALOG")
        self.schema = schema or os.environ.get("DATABRICKS_SCHEMA")

        if not self.server_hostname:
            raise WConnectionError("server_hostname is required")
        if not self.http_path:
            raise WConnectionError("http_path is required")
        if not self.access_token:
            raise WConnectionError("access_token is required")

        self._connection: Optional[Any] = None
        self._thread_local = threading.local()

    @classmethod
    def get_instance(
        cls,
        server_hostname: Optional[str] = None,
        http_path: Optional[str] = None,
        access_token: Optional[str] = None,
        catalog: Optional[str] = None,
        schema: Optional[str] = None,
    ) -> "ConnectionManager":
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls(
                    server_hostname=server_hostname,
                    http_path=http_path,
                    access_token=access_token,
                    catalog=catalog,
                    schema=schema,
                )
            return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        with cls._lock:
            if cls._instance:
                cls._instance.close()
            cls._instance = None

    def get_connection(self) -> Any:
        if not DATABRICKS_SQL_AVAILABLE:
            raise WConnectionError(
                "databricks-sql-connector is not installed. "
                "Install with: pip install databricks-sql-connector"
            )

        if (
            not hasattr(self._thread_local, "connection")
            or self._thread_local.connection is None
        ):
            try:
                self._thread_local.connection = sql.connect(
                    server_hostname=self.server_hostname,
                    http_path=self.http_path,
                    access_token=self.access_token,
                    catalog=self.catalog,
                    schema=self.schema,
                )
            except Exception as e:
                raise WConnectionError(f"Failed to connect to Databricks: {e}")

        return self._thread_local.connection

    def get_cursor(self) -> Any:
        return self.get_connection().cursor()

    def close(self) -> None:
        if hasattr(self._thread_local, "connection") and self._thread_local.connection:
            try:
                self._thread_local.connection.close()
            except Exception:
                pass
            self._thread_local.connection = None

    def commit(self) -> None:
        conn = self.get_connection()
        conn.commit()

    def rollback(self) -> None:
        conn = self.get_connection()
        conn.rollback()

    def ping(self) -> bool:
        try:
            cursor = self.get_cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            return True
        except Exception:
            return False
