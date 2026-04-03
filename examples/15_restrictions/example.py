from typing import Optional
from pydantic import BaseModel, Field
from wdatabricks import WDatabricks

DB_CONFIG = {
    "server_hostname": "your-server.cloud.databricks.com",
    "http_path": "/sql/your-http-path",
    "access_token": "your-access-token",
}


class User(BaseModel):
    id: int = Field(..., description="Primary Key")
    name: str = Field(..., description="NOT NULL")
    email: Optional[str] = Field(None, description="UNIQUE")


def main():
    db = WDatabricks(User, DB_CONFIG)

    print("=== INSERT VALID ===")
    db.insert(User(id=1, name="Alice", email="alice@example.com"))
    print(f"Count: {db.count()}")

    print("\n=== UNIQUE VIOLATION ===")
    try:
        db.insert(User(id=2, name="Bob", email="alice@example.com"))
    except Exception as e:
        print(f"Error: {e}")

    print("\n=== INSERT MORE ===")
    db.insert(User(id=2, name="Bob", email="bob@example.com"))
    print(f"Count: {db.count()}")


if __name__ == "__main__":
    main()
