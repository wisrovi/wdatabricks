from pydantic import BaseModel
from wdatabricks import WDatabricks

DB_CONFIG = {
    "server_hostname": "your-server.cloud.databricks.com",
    "http_path": "/sql/your-http-path",
    "access_token": "your-access-token",
}


class User(BaseModel):
    id: int
    name: str


def main():
    db = WDatabricks(User, DB_CONFIG)
    db.insert(User(id=1, name="Alice"))

    result = db.execute_raw("SELECT COUNT(*) as cnt FROM user")
    print(f"Count: {result}")


if __name__ == "__main__":
    main()
