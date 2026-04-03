from pydantic import BaseModel
from wdatabricks import WDatabricks, QueryBuilder

DB_CONFIG = {
    "server_hostname": "your-server.cloud.databricks.com",
    "http_path": "/sql/your-http-path",
    "access_token": "your-access-token",
}


class User(BaseModel):
    id: int
    name: str
    email: str


class Order(BaseModel):
    id: int
    user_id: int
    amount: float


def main():
    db_user = WDatabricks(User, DB_CONFIG)
    db_order = WDatabricks(Order, DB_CONFIG)
    db_user.sync.create_if_not_exists()
    db_order.sync.create_if_not_exists()

    db_user.insert(User(id=1, name="John", email="john@example.com"))
    db_order.insert(Order(id=1, user_id=1, amount=100.0))

    query = (
        QueryBuilder()
        .select("u.name", "o.amount")
        .from_table("users", "u")
        .join("orders", "o", "u.id = o.user_id")
        .build()
    )
    print(f"Join query: {query}")


if __name__ == "__main__":
    main()
