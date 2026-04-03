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
    db.sync.create_if_not_exists()

    db.insert(User(id=1, name="Alice", email="alice@example.com"))

    def transactional_op(tx):
        db.update(User(id=1, name="Alice Updated", email="alice.updated@example.com"))
        return True

    result = db.with_transaction(transactional_op)
    print(f"Transaction result: {result}")


if __name__ == "__main__":
    main()
