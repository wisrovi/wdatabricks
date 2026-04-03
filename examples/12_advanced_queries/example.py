from pydantic import BaseModel
from wdatabricks import WDatabricks

DB_CONFIG = {
    "server_hostname": "your-server.cloud.databricks.com",
    "http_path": "/sql/your-http-path",
    "access_token": "your-access-token",
}


class Product(BaseModel):
    id: int
    name: str
    price: float


def main():
    db = WDatabricks(Product, DB_CONFIG)
    db.sync.create_if_not_exists()

    products = [
        Product(id=1, name="Laptop", price=999.99),
        Product(id=2, name="Mouse", price=29.99),
        Product(id=3, name="Keyboard", price=89.99),
    ]
    for p in products:
        db.insert(p)

    result = db.execute_raw(
        "SELECT * FROM products WHERE price > (SELECT AVG(price) FROM products)"
    )
    print(f"Above average: {result}")


if __name__ == "__main__":
    main()
