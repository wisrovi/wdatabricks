import sys
import os
import argparse
from typing import Optional

try:
    from databricks import sql

    DATABRICKS_SQL_AVAILABLE = True
except ImportError:
    DATABRICKS_SQL_AVAILABLE = False


def get_connection():
    server_hostname = os.environ.get("DATABRICKS_SERVER_HOSTNAME")
    http_path = os.environ.get("DATABRICKS_HTTP_PATH")
    access_token = os.environ.get("DATABRICKS_ACCESS_TOKEN")

    if not all([server_hostname, http_path, access_token]):
        print("Error: Missing required environment variables.", file=sys.stderr)
        print(
            "Set DATABRICKS_SERVER_HOSTNAME, DATABRICKS_HTTP_PATH, and DATABRICKS_ACCESS_TOKEN",
            file=sys.stderr,
        )
        sys.exit(1)

    if not DATABRICKS_SQL_AVAILABLE:
        print("Error: databricks-sql-connector is not installed.", file=sys.stderr)
        print("Install with: pip install databricks-sql-connector", file=sys.stderr)
        sys.exit(1)

    return sql.connect(
        server_hostname=server_hostname,
        http_path=http_path,
        access_token=access_token,
    )


def cmd_tables(args):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if args.schema:
            cursor.execute(f"SHOW TABLES IN {args.schema}")
        else:
            cursor.execute("SHOW TABLES")
        rows = cursor.fetchall()
        for row in rows:
            print(row[0])
    finally:
        cursor.close()
        conn.close()


def cmd_describe(args):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"DESCRIBE TABLE {args.table}")
        rows = cursor.fetchall()
        print(f"Table: {args.table}")
        print(f"{'Column':<30} {'Type':<20} {'Comment'}")
        print("-" * 60)
        for row in rows:
            print(f"{row[0]:<30} {row[1]:<20} {row[2] if len(row) > 2 else ''}")
    finally:
        cursor.close()
        conn.close()


def cmd_query(args):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(args.query)
        if args.query.strip().upper().startswith("SELECT"):
            rows = cursor.fetchall()
            if cursor.description:
                cols = [d[0] for d in cursor.description]
                print("\t".join(cols))
                print("-" * 80)
                for row in rows:
                    print("\t".join(str(v) for v in row))
            print(f"\n{len(rows)} rows returned")
        else:
            conn.commit()
            print(f"{cursor.rowcount} rows affected")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()


def cmd_test(args):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        if result[0] == 1:
            print("Connection successful!")
            sys.exit(0)
        else:
            print("Connection failed!", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Connection failed: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        prog="wdatabricks",
        description="Databricks SQL CLI tool",
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    tables_parser = subparsers.add_parser("tables", help="List tables")
    tables_parser.add_argument("-s", "--schema", help="Schema name")

    describe_parser = subparsers.add_parser("describe", help="Describe table")
    describe_parser.add_argument("table", help="Table name")

    query_parser = subparsers.add_parser("query", help="Execute SQL query")
    query_parser.add_argument("query", help="SQL query")

    test_parser = subparsers.add_parser("test", help="Test connection")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "tables":
        cmd_tables(args)
    elif args.command == "describe":
        cmd_describe(args)
    elif args.command == "query":
        cmd_query(args)
    elif args.command == "test":
        cmd_test(args)


if __name__ == "__main__":
    main()
