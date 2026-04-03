from pydantic import BaseModel
from wdatabricks import WDatabricks

DB_CONFIG = {
    "server_hostname": "your-server.cloud.databricks.com",
    "http_path": "/sql/your-http-path",
    "access_token": "your-access-token",
}


class Order(BaseModel):
    id: int
    user_id: int
    amount: float


def main():
    db = WDatabricks(Order, DB_CONFIG)
    db.sync.create_if_not_exists()

    for i in range(1, 6):
        db.insert(Order(id=i, user_id=i, amount=float(i * 10)))

    total = db.aggregate("SUM", "amount")
    print(f"Total: {total}")

    count = db.aggregate("COUNT", "id")
    print(f"Count: {count}")

    avg = db.aggregate("AVG", "amount")
    print(f"Average: {avg}")


if __name__ == "__main__":
    main()
