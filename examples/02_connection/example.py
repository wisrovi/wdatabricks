from wdatabricks import ConnectionManager

DB_CONFIG = {
    "server_hostname": "your-server.cloud.databricks.com",
    "http_path": "/sql/your-http-path",
    "access_token": "your-access-token",
}


def main():
    cm = ConnectionManager(**DB_CONFIG)
    with cm.get_connection() as conn:
        print(f"Connected: {conn is not None}")
    cm.close()


if __name__ == "__main__":
    main()
