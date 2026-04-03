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
    email: str


def main():
    db = WDatabricks(User, DB_CONFIG)

    def transaction_operations(tx):
        db.insert(User(id=2, name="Jane", email="jane@example.com"))
        return True

    result = db.with_transaction(transaction_operations)
    print(f"Transaction result: {result}")


if __name__ == "__main__":
    main()
